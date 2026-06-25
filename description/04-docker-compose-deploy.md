# Phần 4 — Docker Compose & Network Isolation

## 4.1 Kiến trúc 4 containers

```
Internet
    │
    │ port 80
    ▼
┌─────────────────────────────────────────┐
│           cinema_frontend network        │
│                                         │
│  ┌──────────────┐    ┌───────────────┐  │
│  │ cinema_nginx │───►│  cinema_web   │  │
│  │ (nginx:alpine│    │ (Django/       │  │
│  │  port 80)    │    │  Gunicorn)    │  │
│  └──────────────┘    └──────┬────────┘  │
└─────────────────────────────│───────────┘
                              │ (cinema_web nằm ở CẢ 2 network)
┌─────────────────────────────│───────────┐
│           cinema_backend network         │
│                             │           │
│                    ┌────────▼────────┐  │
│  ┌──────────────┐  │   cinema_db     │  │
│  │cinema_phpmyadmin│ │ (MySQL 8.0)   │  │
│  │ port 8080    │◄─┤  port 3306      │  │
│  └──────────────┘  │  (ẨN với ngoài)│  │
│                    └─────────────────┘  │
└─────────────────────────────────────────┘
```

## 4.2 Giải thích docker-compose.yml

```yaml
services:
  db:                              # MySQL database
    image: mysql:8.0
    env_file: .env.docker
    volumes:
      - db_data:/var/lib/mysql     # Persistent storage
      - ./cinema.sql:/docker-entrypoint-initdb.d/cinema.sql
    networks:
      - backend                    # ← Chỉ trong backend
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5

  web:                             # Django application
    build: .
    env_file: .env.docker
    depends_on:
      db:
        condition: service_healthy # ← Chờ DB healthy mới start
    networks:
      - frontend                   # ← Giao tiếp với Nginx
      - backend                    # ← Giao tiếp với MySQL
    logging:
      driver: "json-file"
      options:
        max-size: "10m"            # Log rotation 10MB
        max-file: "3"

  nginx:                           # Reverse proxy
    image: nginx:alpine
    ports:
      - "80:80"                    # ← Port duy nhất public
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/static
    networks:
      - frontend                   # ← Chỉ trong frontend
    depends_on:
      - web

  phpmyadmin:                      # DB admin UI
    image: phpmyadmin:latest
    ports:
      - "8080:80"
    env_file: .env.docker
    networks:
      - backend                    # ← Chỉ trong backend
    depends_on:
      - db

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

volumes:
  db_data:
  static_volume:
```

## 4.3 Bảng phân quyền network

| Container | Frontend Network | Backend Network | Public Port |
|---|---|---|---|
| `cinema_nginx` | ✅ | ❌ | **:80** |
| `cinema_web` | ✅ | ✅ | ❌ (nội bộ :8000) |
| `cinema_db` | ❌ | ✅ | ❌ (ẩn hoàn toàn) |
| `cinema_phpmyadmin` | ❌ | ✅ | **:8080** |

### Phân tích bảo mật:

- `cinema_db` **không bao giờ** lộ ra internet — chỉ `cinema_web` và `cinema_phpmyadmin` mới kết nối được
- `cinema_nginx` không thể reach DB trực tiếp — phải đi qua Django
- Nếu Nginx bị compromise, attacker vẫn không thể kết nối MySQL

## 4.4 Kết quả triển khai thực tế

```bash
$ sudo docker ps

NAMES               IMAGE                       STATUS                    PORTS
cinema_nginx        nginx:alpine                Up 29 hours               0.0.0.0:80->80/tcp
cinema_phpmyadmin   phpmyadmin:latest           Up 29 hours               0.0.0.0:8080->80/tcp
cinema_web          website-movies-django-web   Up 29 hours               8000/tcp
cinema_db           mysql:8.0                   Up 29 hours (healthy)     3306/tcp, 33060/tcp
```

### Quan sát quan trọng:

| Container | Ports hiển thị | Ý nghĩa |
|---|---|---|
| `cinema_nginx` | `0.0.0.0:80->80/tcp` | Public — ai cũng truy cập được |
| `cinema_phpmyadmin` | `0.0.0.0:8080->80/tcp` | Public — quản trị DB |
| `cinema_web` | `8000/tcp` | Nội bộ — không có `0.0.0.0:` |
| `cinema_db` | `3306/tcp` | Hoàn toàn ẩn — không lộ ra host |

## 4.5 Truy cập hệ thống

| Dịch vụ | URL | Thông tin |
|---|---|---|
| 🎬 Website | http://35.240.177.27 | Trang chủ Cinema |
| 🗄️ phpMyAdmin | http://35.240.177.27:8080 | User: root / Root@Secure2024 |

## 4.6 Checklist Phần 4

- [x] 4 containers khởi động thành công
- [x] `cinema_db` Status: `(healthy)` — healthcheck hoạt động
- [x] Website trả về HTTP 200
- [x] Network `cinema_frontend` và `cinema_backend` tách biệt
- [x] Log rotation 10MB × 3 files cho `cinema_web`
- [x] Volume `db_data` persistent (dữ liệu không mất khi restart)
- [x] `cinema_web` phụ thuộc `cinema_db` healthy mới start
