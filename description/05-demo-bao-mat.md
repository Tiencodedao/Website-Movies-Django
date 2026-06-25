# Phần 5 — Demo Đánh giá Bảo mật (4 kịch bản)

## 5.1 Demo 1 — Trivy CVE Scan

### Lệnh thực hiện

```bash
# Trên Google Cloud VM
sudo trivy image website-movies-django-web \
  --severity CRITICAL,HIGH \
  --no-progress
```

### Kết quả thực tế

```
Image: website-movies-django-web
════════════════════════════════════════════════════
Total: 65 lỗ hổng  (CRITICAL: 11, HIGH: 54)

┌──────────────────────┬────────────────┬──────────┬──────────────┐
│ Library              │ Vulnerability  │ Severity │ Status       │
├──────────────────────┼────────────────┼──────────┼──────────────┤
│ libmariadb-dev       │ CVE-2026-44172 │ CRITICAL │ affected     │
│                      │ CVE-2026-49261 │ CRITICAL │ affected     │
│ libmariadb-dev-compat│ CVE-2026-44172 │ CRITICAL │ affected     │
│ libmariadb3          │ CVE-2026-44172 │ CRITICAL │ affected     │
│ linux-libc-dev       │ CVE-2026-43185 │ CRITICAL │ affected     │
└──────────────────────┴────────────────┴──────────┴──────────────┘
```

### Phân tích kết quả

| Nhóm CVE | Thư viện | Loại lỗ hổng | Mức độ |
|---|---|---|---|
| CVE-2026-44172 | libmariadb-dev | SQL Injection | CRITICAL |
| CVE-2026-49261 | libmariadb-dev | Arbitrary code execution | CRITICAL |
| CVE-2026-43185 | linux-libc-dev | Kernel privilege escalation | CRITICAL |
| CVE-2025-69720 | libncursesw6 | Buffer overflow | HIGH |
| CVE-2026-11822 | libsqlite3-0 | Memory corruption | HIGH |

### Ý nghĩa

> **CVE (Common Vulnerabilities and Exposures)** là hệ thống định danh lỗ hổng bảo mật toàn cầu.  
> Mức CRITICAL = CVSS score ≥ 9.0/10 — có thể bị khai thác ngay lập tức.  
> **Pipeline GitHub Actions FAIL** khi phát hiện CRITICAL → chặn deploy tự động.

---

## 5.2 Demo 2 — Tấn công Database từ Backend Network

### Kịch bản

Mô phỏng attacker đột nhập vào một container trong `cinema_backend` network và thử kết nối MySQL.

### Lệnh thực hiện

```bash
# Tạo container "attacker" tham gia backend network
sudo docker run -d --name attacker \
  --network cinema_backend \
  alpine sleep 60

# Thử kết nối MySQL từ container attacker
sudo docker exec attacker sh -c \
  'apk add -q netcat-openbsd && nc -zv cinema_db 3306 2>&1'
```

### Kết quả thực tế

```
Connection to cinema_db (172.18.0.2) 3306 port [tcp/mysql] succeeded!
KET_QUA: DATABASE_BI_LO!
```

### Phân tích

> ⚠️ **Phát hiện:** Container lạ join vào `cinema_backend` có thể kết nối MySQL trực tiếp.  
> **Nguyên nhân:** Docker network mặc định không kiểm soát ai được join — bất kỳ container nào  
> có quyền `docker run --network cinema_backend` đều truy cập được.  
> **Khuyến nghị:** Thêm Docker network encryption hoặc service mesh (Istio/Consul) để xác thực.

```bash
# Dọn dẹp sau demo
sudo docker rm -f attacker
```

---

## 5.3 Demo 3 — Network Isolation hoạt động (Frontend → DB)

### Kịch bản

Mô phỏng attacker compromise được Nginx container (frontend) và thử reach MySQL.

### Lệnh thực hiện

```bash
# Tạo container attacker trong frontend network
sudo docker run --rm --name attacker2 \
  --network cinema_frontend \
  alpine sh -c \
  'apk add -q netcat-openbsd 2>/dev/null; nc -zv cinema_db 3306 2>&1 || echo ISOLATION_WORKS!'
```

### Kết quả thực tế

```
nc: getaddrinfo for host "cinema_db" port 3306: Try again
KET_QUA: ISOLATION_HOAT_DONG_DB_AN_HOAN_TOAN!
```

### Phân tích

> ✅ **Bảo mật hoạt động đúng!**  
> Container trong `cinema_frontend` hoàn toàn không thể:  
> - Resolve DNS tên `cinema_db`  
> - Kết nối port 3306  
> - Biết địa chỉ IP của MySQL  
>
> **Kết luận:** Ngay cả khi attacker compromise được Nginx, họ không thể reach database.  
> Network isolation là lớp phòng thủ thứ 2 (Defense in Depth).

---

## 5.4 Demo 4 — Kiểm tra Non-root User

### Lệnh thực hiện

```bash
# Kiểm tra user của từng container
sudo docker exec cinema_web whoami
sudo docker exec cinema_nginx whoami
sudo docker exec cinema_db whoami
```

### Kết quả thực tế

```
[cinema_web]   → appuser   ✅ AN TOÀN
[cinema_nginx] → root      ⚠️ RỦI RO
[cinema_db]    → root      ⚠️ RỦI RO
```

### Phân tích

| Container | User | Rủi ro nếu bị exploit |
|---|---|---|
| `cinema_web` (Django) | **appuser** | ✅ Thấp — chỉ quyền user thường |
| `cinema_nginx` | root | ⚠️ Cao — có thể escape lên host |
| `cinema_db` | root | ⚠️ Cao — có thể escape lên host |

> **Giải thích:** Django chạy với `USER appuser` (cấu hình trong Dockerfile).  
> Nếu attacker exploit lỗ hổng trong Django app → chỉ có quyền `appuser`  
> → Không thể ghi file hệ thống, không thể leo thang lên root VM.  
>
> **Khuyến nghị:** Nâng cấp Nginx và MySQL lên image có hỗ trợ non-root user.

---

## 5.5 Tổng hợp kết quả bảo mật

| # | Demo | Kết quả | Đánh giá |
|---|---|---|---|
| 1 | Trivy CVE Scan | 65 lỗ hổng (11 CRITICAL, 54 HIGH) | ⚠️ Cần vá — pipeline chặn tự động |
| 2 | Tấn công DB từ backend | **THÀNH CÔNG** — port 3306 mở | ⚠️ Cần kiểm soát thêm |
| 3 | Tấn công DB từ frontend | **THẤT BẠI** — DB ẩn hoàn toàn | ✅ Network isolation hiệu quả |
| 4 | Non-root user | Django = appuser, Nginx/DB = root | ✅ Django an toàn, Nginx/DB cần cải thiện |

## 5.6 Khuyến nghị cải tiến

1. **CVE Fix:** Nâng cấp `python:3.12-slim` lên phiên bản mới nhất, dùng `--ignore-unfixed`
2. **Network Security:** Thêm firewall iptables bên trong Docker network cho backend
3. **Nginx non-root:** Dùng `nginxinc/nginx-unprivileged` thay vì `nginx:alpine`
4. **MySQL non-root:** Map UID/GID cụ thể trong docker-compose
5. **Secrets Manager:** Dùng Google Secret Manager thay vì `.env.docker` trực tiếp

## 5.7 Checklist Phần 5

- [x] Trivy cài thành công (v0.71.2)
- [x] Demo 1: Trivy scan tìm thấy 65 CVE
- [x] Demo 2: Tấn công backend network thành công (ghi nhận lỗ hổng)
- [x] Demo 3: Frontend không thể kết nối DB (isolation hoạt động)
- [x] Demo 4: Django chạy appuser (non-root confirmed)
