# 📚 Tài liệu DevSecOps — Hệ thống Cinema Django

> **Đề tài:** Đánh giá an ninh và bảo mật cho hệ thống Docker Container  
> **Dự án:** Website đặt vé xem phim (Cinema Django)  
> **Repository:** https://github.com/Tiencodedao/Website-Movies-Django

---

## 🗂️ Cấu trúc tài liệu

| File | Nội dung |
|---|---|
| [01-cau-truc-du-an.md](./01-cau-truc-du-an.md) | Cấu trúc project, Dockerfile, docker-compose |
| [02-github-actions-pipeline.md](./02-github-actions-pipeline.md) | CI/CD pipeline, Trivy scan tự động |
| [03-google-cloud-vm.md](./03-google-cloud-vm.md) | Tạo VM, cài Docker, triển khai |
| [04-docker-compose-deploy.md](./04-docker-compose-deploy.md) | 4 containers, network isolation |
| [05-demo-bao-mat.md](./05-demo-bao-mat.md) | 4 kịch bản demo tấn công & phòng thủ |
| [BAO-CAO-TONG-HOP.md](./BAO-CAO-TONG-HOP.md) | **File tổng hợp để viết báo cáo** |

---

## 🏗️ Kiến trúc hệ thống

```
Developer (Local)
      │  git push
      ▼
GitHub Repository
      │
      ▼
GitHub Actions (security.yml)
      │
      ├─► Build Docker Image
      ├─► Trivy Scan (CVE / Misconfiguration)
      ├─► Security Validation (FAIL nếu có CRITICAL)
      └─► [Nếu pass] Deploy
            │
            ▼
Google Cloud VM (Ubuntu 22.04 — 35.240.177.27)
      │
      ▼
Docker Compose
      │
      ├── Nginx Container        (frontend network — port 80)
      ├── Django Web Container   (frontend + backend network)
      ├── MySQL Container        (backend network — ẩn)
      └── phpMyAdmin Container   (backend network — port 8080)
```

---

## ✅ Kết quả đạt được

| Hạng mục | Kết quả |
|---|---|
| CVE phát hiện | **65 lỗ hổng** (CRITICAL: 11, HIGH: 54) |
| Pipeline bảo mật | **FAIL** tự động khi có CRITICAL |
| Network Isolation | **Hoạt động** — frontend không thấy DB |
| Non-root User | Django chạy với **appuser** |
| Website Live | **http://35.240.177.27** |
| phpMyAdmin | **http://35.240.177.27:8080** |
