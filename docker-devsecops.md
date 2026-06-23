# Đề tài: Đánh giá an ninh và bảo mật cho hệ thống Docker Container của ứng dụng đặt vé xem phim Django

## 1. Giới thiệu

Mục tiêu của đề tài là xây dựng môi trường triển khai thực tế cho ứng dụng đặt vé xem phim sử dụng Django trên nền tảng Docker, đồng thời đánh giá các rủi ro bảo mật liên quan đến Docker Image và giao tiếp mạng giữa các Container.

Hệ thống được tích hợp quy trình DevSecOps thông qua GitHub Actions và Trivy nhằm tự động phát hiện lỗ hổng bảo mật trước khi triển khai lên máy chủ Google Cloud.

---

# 2. Kiến trúc hệ thống

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Build Docker Image
    |
    +--> Trivy Scan (CVE / Misconfiguration)
    |
    +--> Security Validation (Fail nếu có Critical)
    |
    +--> Deploy
    |
    v
Google Cloud VM (Ubuntu 22.04)
    |
Docker Compose
    |
+--------------------------------------------+
| Nginx Container        (frontend network)  |
| Django Web Container   (frontend + backend)|
| MySQL Container        (backend network)   |
| phpMyAdmin Container   (backend network)   |
+--------------------------------------------+
```

---

# 3. Thành phần hệ thống

## Django Web

Chứa toàn bộ chức năng:

* Đăng ký tài khoản
* Đăng nhập
* Quản lý phim
* Đặt vé
* Thanh toán (mô phỏng)
* REST API cho ứng dụng Mobile (Flutter)

## MySQL 8.0

Lưu trữ:

* Người dùng
* Vé
* Lịch chiếu
* Thông tin phim

## Nginx

Reverse proxy:

* Phục vụ static files
* Forward request tới Django (Gunicorn)

## phpMyAdmin

Công cụ quản trị database qua giao diện web (chỉ dùng trong môi trường dev/demo).

## GitHub Actions

Tự động:

* Build Image
* Quét bảo mật (Trivy)
* Deploy

## Trivy

Quét:

* CVE (Common Vulnerabilities and Exposures)
* Vulnerability
* Misconfiguration
* Secret leaks

---

# 4. Triển khai Docker

## Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cài dependencies hệ thống cho mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Chạy với non-root user (bảo mật)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

ENV SECRET_KEY=build-time-placeholder-not-used-in-production
ENV DEBUG=False
ENV ALLOWED_HOSTS=*
RUN python manage.py collectstatic --noinput

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
```

---

## docker-compose.yml

```yaml
services:

  db:
    image: mysql:8.0
    container_name: cinema_db
    restart: unless-stopped
    env_file: .env.docker
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-pRoot@Secure2024"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - db_data:/var/lib/mysql
      - ./cinema.sql:/docker-entrypoint-initdb.d/01_cinema.sql
    networks:
      - backend          # DB chỉ nằm trong network nội bộ backend

  web:
    build: .
    container_name: cinema_web
    restart: unless-stopped
    env_file: .env.docker
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - "8000"
    networks:
      - frontend         # Nginx truy cập Django qua đây
      - backend          # Django truy cập MySQL qua đây
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    container_name: cinema_nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    depends_on:
      - web
    networks:
      - frontend         # Nginx chỉ nằm trong frontend, KHÔNG thấy DB

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: cinema_phpmyadmin
    restart: unless-stopped
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
      PMA_USER: root
      PMA_PASSWORD: Root@Secure2024
    ports:
      - "8080:80"
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend          # phpMyAdmin cần truy cập DB (backend only)

volumes:
  db_data:
    name: cinema_db_data
  static_volume:
    name: cinema_static
  media_volume:
    name: cinema_media

networks:
  frontend:
    driver: bridge
    name: cinema_frontend
  backend:
    driver: bridge
    name: cinema_backend
```

**Nguyên tắc Network Isolation:**

| Container     | frontend | backend | Ghi chú                              |
|---------------|----------|---------|--------------------------------------|
| nginx         | ✅       | ❌      | Chỉ thấy Django, không thấy DB       |
| web (Django)  | ✅       | ✅      | Cầu nối giữa frontend và backend     |
| db (MySQL)    | ❌       | ✅      | Hoàn toàn ẩn với thế giới bên ngoài  |
| phpmyadmin    | ❌       | ✅      | Quản trị DB, không expose ra ngoài   |

---

# 5. Kịch bản Demo

## Bước 1 - Thiết lập môi trường

Tạo VM Ubuntu trên Google Cloud.

Cài Docker:

```bash
sudo apt update
sudo apt install docker.io -y
```

Cài Docker Compose:

```bash
sudo apt install docker-compose-plugin -y
```

Clone source:

```bash
git clone <repository>
cd MOVIE-WEBSITES-2
```

Khởi động:

```bash
docker compose up -d --build
```

Kiểm tra:

```bash
docker ps
```

Kết quả mong đợi:

```
CONTAINER ID   NAME               STATUS          PORTS
xxxxxxxxxxxx   cinema_nginx       Up              0.0.0.0:80->80/tcp
xxxxxxxxxxxx   cinema_web         Up              8000/tcp
xxxxxxxxxxxx   cinema_db          Up (healthy)    3306/tcp
xxxxxxxxxxxx   cinema_phpmyadmin  Up              0.0.0.0:8080->80/tcp
```

---

## Bước 2 - Kiểm thử bảo mật

### Demo 1: Quét Docker Image bằng Trivy

```bash
# Cài Trivy
sudo apt install wget apt-transport-https gnupg -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb generic main" \
  | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install trivy -y

# Quét image
trivy image cinema_web
```

Thu thập kết quả theo mức độ:

* **CRITICAL** — Nghiêm trọng nhất, phải vá ngay
* **HIGH** — Rủi ro cao
* **MEDIUM** — Rủi ro trung bình
* **LOW** — Rủi ro thấp

---

### Demo 2: Thử tấn công Database từ container lạ (TRƯỚC khi cô lập mạng)

Tạo container attacker (không thuộc hệ thống):

```bash
docker run -it --name attacker --network cinema_backend alpine sh
```

Bên trong container attacker, cài netcat:

```bash
apk add netcat-openbsd
```

Thử kết nối MySQL (port 3306):

```bash
nc -zv cinema_db 3306
```

Nếu thành công → **Database bị lộ** và có thể bị tấn công từ container lạ.

Dọn dẹp:

```bash
docker rm -f attacker
```

---

## Bước 3 - Phòng thủ

### Tích hợp Trivy vào GitHub Actions

File: `.github/workflows/security.yml`

```yaml
name: Security Pipeline — DevSecOps

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  trivy-scan:
    name: Trivy Security Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t cinema-app:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: cinema-app:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH
          exit-code: 1          # Fail pipeline nếu có CRITICAL

      - name: Upload Trivy scan results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-results.sarif
```

**Nguyên tắc:**

* Có `CRITICAL` → Pipeline **FAIL** → Không deploy
* Không có `CRITICAL` → Pipeline **PASS** → Tiến hành deploy

---

### Docker Network Isolation

Như đã cấu hình trong `docker-compose.yml`:

* Database (`cinema_db`) chỉ nằm trong network `backend`
* Nginx chỉ nằm trong network `frontend`
* Django nằm ở cả hai để làm cầu nối
* Không có container nào từ bên ngoài có thể truy cập DB trực tiếp

---

## Bước 4 - Kiểm tra lại sau khi áp dụng phòng thủ

### Kiểm tra Trivy sau khi vá lỗ hổng

```bash
trivy image cinema_web --severity CRITICAL
```

Kết quả mong muốn:

```
Total: 0 (CRITICAL: 0)
```

### Kiểm tra Network Isolation

Thử tấn công lại từ container KHÔNG thuộc backend network:

```bash
docker run --rm --name attacker2 \
  --network cinema_frontend \
  alpine sh -c "apk add -q netcat-openbsd && nc -zv cinema_db 3306"
```

Kết quả mong đợi:

```text
nc: getaddrinfo for host "cinema_db" port 3306: Name does not resolve
```

Hoặc:

```text
Connection refused
```

→ **Database hoàn toàn bị cô lập** với container không hợp lệ.

### Kiểm tra ứng dụng vẫn hoạt động bình thường

```bash
curl -I http://localhost:80
```

Kết quả:

```
HTTP/1.1 200 OK
```

---

# 6. Kết quả đạt được

* ✅ Website hoạt động công khai trên Internet (port 80 qua Nginx).
* ✅ Docker Image được quét tự động bằng Trivy mỗi lần push code.
* ✅ Lỗ hổng nghiêm trọng (CRITICAL) bị chặn trước khi Deploy.
* ✅ Database MySQL được cô lập hoàn toàn trong network `backend`.
* ✅ Non-root user trong container tăng cường bảo mật runtime.
* ✅ Kết quả scan hiển thị trực tiếp trên GitHub Security tab.

---

# 7. Thông tin cấu hình

## Ports (Local / Dev)

| Service    | Port Host | Port Container | Ghi chú              |
|------------|-----------|----------------|----------------------|
| Nginx      | 80        | 80             | Public entry point   |
| phpMyAdmin | 8080      | 80             | Quản trị DB (dev)    |
| MySQL      | 3307      | 3306           | Chỉ dùng local debug |
| Django     | —         | 8000           | Nội bộ, qua Nginx    |

## Credentials (Dev/Demo — thay đổi khi production)

| Service | Username | Password        |
|---------|----------|-----------------|
| MySQL root | root  | Root@Secure2024 |
| MySQL app  | root  | Root@Secure2024 |
| DB name    | —     | cinema          |

## Tech Stack

| Layer        | Technology           |
|--------------|----------------------|
| Web Framework | Django 6.0.4        |
| WSGI Server  | Gunicorn 21.2.0      |
| Database     | MySQL 8.0            |
| DB Client    | mysqlclient 2.2.8    |
| Reverse Proxy | Nginx:alpine        |
| Container    | Docker + Compose     |
| Security Scan | Trivy (Aqua Security)|
| CI/CD        | GitHub Actions       |
| Cloud        | Google Cloud VM (Ubuntu 22.04) |

---

# 8. Kết luận

Giải pháp Docker DevSecOps với Django + MySQL phù hợp cho doanh nghiệp vừa và nhỏ nhờ:

* Triển khai nhanh với Docker Compose
* Chi phí thấp (Google Cloud VM)
* Dễ quản trị qua phpMyAdmin
* Bảo mật tự động qua GitHub Actions + Trivy
* Network isolation ngăn chặn lateral movement
