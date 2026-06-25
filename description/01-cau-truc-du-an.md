# Phần 1 — Cấu trúc Dự án & Bảo mật Code

## 1.1 Tổng quan

Dự án là website đặt vé xem phim xây dựng bằng Django, được container hóa bằng Docker và triển khai trên Google Cloud.

## 1.2 Cấu trúc thư mục

```
Website-Movies-Django/
├── .github/
│   └── workflows/
│       └── security.yml       ← GitHub Actions CI/CD pipeline
├── description/               ← Tài liệu hướng dẫn (thư mục này)
├── nginx/
│   └── nginx.conf             ← Cấu hình Nginx reverse proxy
├── cinema_django/             ← Django settings, urls
├── movies/                    ← App Django chính (models, views)
├── templates/                 ← HTML templates
├── static/                    ← CSS, JS, Images
├── Dockerfile                 ← Build Django image
├── docker-compose.yml         ← Orchestrate 4 containers
├── entrypoint.sh              ← Script khởi động Gunicorn
├── requirements.txt           ← Python dependencies
├── .env.docker                ← Secrets (KHÔNG commit GitHub!)
├── .gitignore                 ← Danh sách file bị bỏ qua
└── demo-security-test.sh      ← Script demo bảo mật
```

## 1.3 Phân tích Dockerfile (bảo mật)

```dockerfile
FROM python:3.12-slim           # Base image tối giản (giảm attack surface)

# Cài dependencies hệ thống
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*    # Xóa cache giảm kích thước image

WORKDIR /app

# Copy và cài Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Thu thập static files (dùng dummy SECRET_KEY)
RUN SECRET_KEY=build-time-dummy python manage.py collectstatic --noinput

# ✅ BẢO MẬT: Tạo user non-root
RUN addgroup --system appgroup && adduser --system --group appuser

# ✅ BẢO MẬT: Chạy với user appuser (không phải root)
USER appuser

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
```

### Giải thích bảo mật:

| Kỹ thuật | Mục đích |
|---|---|
| `python:3.12-slim` | Image nhỏ, ít package → ít lỗ hổng hơn |
| `rm -rf /var/lib/apt/lists/*` | Xóa cache apt, giảm kích thước layer |
| `--no-cache-dir` | Không cache pip, giảm kích thước |
| `USER appuser` | **Không chạy root** → nếu bị exploit chỉ có quyền user |
| `EXPOSE 8000` | Chỉ expose port cần thiết |

## 1.4 File .gitignore (bảo vệ secrets)

```gitignore
# Secrets — KHÔNG BAO GIỜ commit lên GitHub
.env
.env.*
.env.docker
*.env

# Database
db.sqlite3

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# Logs
*.log
```

### Lý do quan trọng:

> ⚠️ **Secret leakage** là một trong những lỗi bảo mật phổ biến nhất.  
> Nếu `SECRET_KEY`, `DB_PASSWORD` bị commit lên GitHub public repo,  
> attacker có thể tìm thấy qua Google hoặc GitHub search trong vài giây!

## 1.5 File .env.docker (quản lý secrets)

File này **không có trong repository** — phải tạo thủ công trên server:

```env
SECRET_KEY=cinema-production-secret-key-2024
DEBUG=False
ALLOWED_HOSTS=35.240.177.27,localhost,127.0.0.1

DB_HOST=db
DB_NAME=cinema
DB_USER=root
DB_PASSWORD=Root@Secure2024
DB_PORT=3306

MYSQL_ROOT_PASSWORD=Root@Secure2024
MYSQL_DATABASE=cinema

PMA_HOST=db
PMA_PORT=3306
PMA_USER=root
PMA_PASSWORD=Root@Secure2024
```

## 1.6 Checklist Phần 1

- [x] `.gitignore` đã cấu hình đúng
- [x] `.env.docker` không có trong git history
- [x] `Dockerfile` dùng non-root user
- [x] Base image tối giản (`python:3.12-slim`)
- [x] Secrets được quản lý qua environment variables
