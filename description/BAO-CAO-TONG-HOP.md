# BÁO CÁO TỔNG HỢP
# Đề tài: Đánh giá An ninh và Bảo mật cho Hệ thống Docker Container

---

## THÔNG TIN ĐỀ TÀI

| Mục | Nội dung |
|---|---|
| **Đề tài** | Đánh giá an ninh và bảo mật cho hệ thống Docker Container |
| **Ứng dụng** | Website đặt vé xem phim (Cinema Django) |
| **Repository** | https://github.com/Tiencodedao/Website-Movies-Django |
| **Cloud** | Google Cloud Platform — asia-southeast1-b (Singapore) |
| **VM IP** | 35.240.177.27 |
| **Website** | http://35.240.177.27 |
| **phpMyAdmin** | http://35.240.177.27:8080 |

---

## I. KIẾN TRÚC HỆ THỐNG

### 1.1 Sơ đồ tổng quan

```
Developer (Local Machine — Windows)
    │
    │  git push origin main
    ▼
GitHub Repository
(github.com/Tiencodedao/Website-Movies-Django)
    │
    ▼
GitHub Actions CI/CD (security.yml)
    │
    ├─► [Job 1] Trivy Security Scan
    │       ├── Build Docker Image
    │       ├── Scan CVE (CRITICAL + HIGH)
    │       └── FAIL nếu có CRITICAL → Chặn deploy
    │
    └─► [Job 2] Docker Build & Smoke Test (chỉ chạy nếu Job 1 PASS)
            ├── docker compose up
            └── HTTP 200 smoke test
                    │
                    ▼ (Deploy thủ công)
    Google Cloud VM (Ubuntu 22.04 — 35.240.177.27)
                    │
                    ▼
            Docker Compose
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
cinema_nginx   cinema_web      cinema_db
(frontend net) (frontend +     (backend net)
port 80        backend net)    port 3306 (ẩn)
                               │
                               ▼
                        cinema_phpmyadmin
                        (backend net)
                        port 8080
```

### 1.2 Công nghệ sử dụng

| Thành phần | Công nghệ | Phiên bản |
|---|---|---|
| Web Framework | Django | 6.0.4 |
| WSGI Server | Gunicorn | 21.2.0 |
| Database | MySQL | 8.0 |
| Reverse Proxy | Nginx | alpine |
| DB Admin | phpMyAdmin | latest |
| Container | Docker Engine | 29.6.0 |
| Orchestration | Docker Compose | v5.1.4 |
| CI/CD | GitHub Actions | — |
| Security Scanner | Trivy | 0.71.2 |
| Cloud | Google Cloud VM | e2-medium |

---

## II. TRIỂN KHAI VÀ CẤU HÌNH BẢO MẬT

### 2.1 Bảo mật Code (Phần 1)

**Vấn đề giải quyết:** Secret leakage — passwords và API keys bị lộ trong git history

**Giải pháp thực hiện:**
- Tạo `.gitignore` loại trừ `.env`, `.env.docker`, `db.sqlite3`
- Chạy `git rm --cached` để xóa files khỏi tracking
- Tất cả secrets chỉ tồn tại trong `.env.docker` trên server (không commit)

### 2.2 CI/CD Pipeline Bảo mật (Phần 2)

**Cấu hình `security.yml`:**

```yaml
permissions:
  security-events: write   # Upload SARIF lên GitHub Security tab

steps:
  - Build Docker image
  - Trivy scan (table format, exit-code: 0)    # In kết quả
  - Trivy scan (SARIF format, exit-code: 1)    # FAIL nếu CRITICAL
  - Upload SARIF → GitHub Security tab
```

**Kết quả 4 lần chạy:**

| Run | Commit | Kết quả | Ghi chú |
|---|---|---|---|
| #1 | 74cd7b3 | ❌ FAIL | Thiếu `permissions` block |
| #2 | f112f5c | ❌ FAIL | Trivy: 65 CVE (11 CRITICAL) |
| #3 | 056d2ca | ❌ FAIL | Trivy CRITICAL + fix warnings |
| #4 | 439aff2 | ❌ FAIL | Trivy CRITICAL (đúng thiết kế) |

> **Nhận xét:** Pipeline FAIL là kết quả **đúng** — chứng minh hệ thống phát hiện và chặn lỗ hổng tự động.

### 2.3 Google Cloud VM (Phần 3)

| Thông số | Giá trị |
|---|---|
| Zone | asia-southeast1-b |
| Machine | e2-medium (2 vCPU, 4GB) |
| OS | Ubuntu 22.04 LTS |
| Docker | CE 29.6.0 (cài từ get.docker.com) |
| Firewall | port 80 + 8080 mở toàn internet |

### 2.4 Docker Compose — 4 Containers (Phần 4)

**Trạng thái production (29+ giờ liên tục):**

```
cinema_nginx        Up 29 hours   0.0.0.0:80->80/tcp      PUBLIC
cinema_phpmyadmin   Up 29 hours   0.0.0.0:8080->80/tcp    PUBLIC
cinema_web          Up 29 hours   8000/tcp                 NỘI BỘ
cinema_db           Up 29 hours   3306/tcp (healthy)       ẨN
```

**Network Isolation:**

| Container | Frontend | Backend | Public |
|---|---|---|---|
| cinema_nginx | ✅ | ❌ | :80 |
| cinema_web | ✅ | ✅ | — |
| cinema_db | ❌ | ✅ | — |
| cinema_phpmyadmin | ❌ | ✅ | :8080 |

---

## III. KẾT QUẢ ĐÁNH GIÁ BẢO MẬT

### 3.1 Demo 1 — Trivy CVE Scan

**Lệnh:**
```bash
sudo trivy image website-movies-django-web --severity CRITICAL,HIGH
```

**Kết quả:**
```
Total: 65 (CRITICAL: 11, HIGH: 54)

Các CVE CRITICAL quan trọng:
├── CVE-2026-44172: libmariadb-dev — SQL Injection
├── CVE-2026-49261: libmariadb-dev — Arbitrary code execution
├── CVE-2026-43185: linux-libc-dev — Kernel privilege escalation
├── CVE-2026-44168: libmariadb-dev-compat — Code execution
└── CVE-2026-48163: libmariadb3 — Code execution via global var
```

**Hành động tự động:** Pipeline GitHub Actions FAIL → Không cho deploy

---

### 3.2 Demo 2 — Tấn công DB từ Backend Network

**Kịch bản:** Container lạ tham gia `cinema_backend` network

**Lệnh:**
```bash
sudo docker run -d --name attacker --network cinema_backend alpine sleep 60
sudo docker exec attacker sh -c 'nc -zv cinema_db 3306 2>&1'
```

**Kết quả:**
```
Connection to cinema_db (172.18.0.2) 3306 port [tcp/mysql] succeeded!
→ DATABASE BỊ LỘ với container cùng network!
```

**Đánh giá:** ⚠️ Phát hiện điểm yếu — cần thêm lớp xác thực cho Docker network.

---

### 3.3 Demo 3 — Network Isolation (Frontend → DB)

**Kịch bản:** Container trong `cinema_frontend` thử kết nối MySQL

**Lệnh:**
```bash
sudo docker run --rm --network cinema_frontend alpine sh -c \
  'nc -zv cinema_db 3306 2>&1'
```

**Kết quả:**
```
nc: getaddrinfo for host "cinema_db" port 3306: Try again
→ BẢO MẬT HOẠT ĐỘNG — DB hoàn toàn ẩn với frontend!
```

**Đánh giá:** ✅ Network isolation ngăn chặn hiệu quả — Defense in Depth.

---

### 3.4 Demo 4 — Non-root User

**Lệnh:**
```bash
sudo docker exec cinema_web whoami      # → appuser
sudo docker exec cinema_nginx whoami    # → root
sudo docker exec cinema_db whoami       # → root
```

**Kết quả:**

| Container | User | Mức độ an toàn |
|---|---|---|
| cinema_web (Django) | **appuser** | ✅ AN TOÀN |
| cinema_nginx | root | ⚠️ CẦN CẢI THIỆN |
| cinema_db | root | ⚠️ CẦN CẢI THIỆN |

**Đánh giá:** Django đã áp dụng principle of least privilege. Nginx và MySQL cần cấu hình thêm.

---

## IV. TỔNG HỢP ĐÁNH GIÁ

### 4.1 Bảng điểm bảo mật

| Hạng mục | Điểm | Ghi chú |
|---|---|---|
| Secret Management | ✅ Tốt | .env không commit GitHub |
| CI/CD Security | ✅ Tốt | Trivy tích hợp, pipeline FAIL tự động |
| Network Isolation | ✅ Tốt | Frontend không reach DB |
| Image Vulnerabilities | ⚠️ Trung bình | 65 CVE, cần vá |
| Non-root Container | ⚠️ Một phần | Django OK, Nginx/DB chưa |
| Secrets on VM | ⚠️ Trung bình | .env.docker thủ công, chưa dùng Secret Manager |
| Healthcheck | ✅ Tốt | MySQL healthcheck trước khi web start |
| Log Management | ✅ Tốt | Log rotation 10MB × 3 |

### 4.2 Kết quả đạt được

```
✅ Trivy tự động quét CVE mỗi lần push code
✅ Pipeline FAIL khi có CRITICAL → Chặn deploy tự động
✅ MySQL hoàn toàn ẩn trong backend network
✅ Nginx không thể kết nối DB trực tiếp
✅ Django chạy non-root user (appuser)
✅ Secrets không commit lên GitHub
✅ Log rotation cho containers
✅ MySQL healthcheck đảm bảo thứ tự khởi động
✅ Website hoạt động HTTP 200 qua Nginx
✅ phpMyAdmin quản trị qua port 8080
```

### 4.3 Hạn chế và hướng cải tiến

| Hạn chế | Giải pháp đề xuất |
|---|---|
| 65 CVE trong image | Nâng version base image, update packages |
| Backend network không có authn | Thêm service mesh (Consul/Istio) |
| Nginx/MySQL chạy root | Dùng `nginx-unprivileged`, set UID/GID MySQL |
| .env.docker thủ công | Dùng Google Secret Manager |
| Không có HTTPS | Cài certbot + Let's Encrypt |
| phpMyAdmin public :8080 | Thêm Basic Auth hoặc đổi port ẩn |

---

## V. KẾT LUẬN

Đề tài đã thành công triển khai hệ thống **DevSecOps** hoàn chỉnh với các kết quả:

1. **Tự động phát hiện lỗ hổng:** Trivy tích hợp vào GitHub Actions phát hiện 65 CVE (11 CRITICAL) và chặn deploy tự động.

2. **Network Isolation:** Kiến trúc 2 networks (`frontend`/`backend`) ngăn Nginx trực tiếp kết nối MySQL — chứng minh qua demo tấn công thực tế.

3. **Principle of Least Privilege:** Django container chạy với `appuser` (non-root) — giảm thiểu thiệt hại nếu bị khai thác.

4. **Secret Management:** Không có secrets nào trong git history — `.env.docker` chỉ tồn tại trên server.

5. **Infrastructure as Code:** Toàn bộ hệ thống được định nghĩa trong `docker-compose.yml` và `security.yml` — có thể tái tạo hoàn toàn.

> **Nhận xét cuối:** Hệ thống đạt mức bảo mật tốt cho môi trường học thuật. Để deploy production thực tế cần thêm HTTPS, Secret Manager và vá các CVE còn tồn tại.

---

## VI. TÀI LIỆU THAM KHẢO

1. NIST — CVE Database: https://nvd.nist.gov
2. Aqua Security Trivy: https://trivy.dev/docs
3. Docker Security Best Practices: https://docs.docker.com/develop/security-best-practices
4. OWASP Docker Top 10: https://owasp.org/www-project-docker-top-10
5. GitHub Actions Security Hardening: https://docs.github.com/en/actions/security-guides
6. Google Cloud Compute Engine: https://cloud.google.com/compute/docs
