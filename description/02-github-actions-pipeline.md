# Phần 2 — GitHub Actions CI/CD Pipeline Bảo mật

## 2.1 Tổng quan pipeline

GitHub Actions tự động chạy mỗi khi có `git push` lên nhánh `main` hoặc `develop`.

```
git push
    │
    ▼
GitHub Actions kích hoạt
    │
    ├─► Job 1: trivy-scan
    │       ├── Checkout code
    │       ├── Build Docker image
    │       ├── Trivy scan (table format — xem log)
    │       ├── Trivy scan (SARIF — upload Security tab)
    │       └── Upload kết quả lên GitHub Security tab
    │
    └─► Job 2: docker-build-test (chỉ chạy nếu Job 1 PASS)
            ├── Checkout code
            ├── Tạo .env.docker test
            ├── docker compose up -d
            ├── Smoke test HTTP 200
            └── docker compose down
```

## 2.2 Nội dung file security.yml

```yaml
name: Security Pipeline — DevSecOps

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Cấp quyền cho workflow
permissions:
  contents: read
  security-events: write   # Upload SARIF lên Security tab
  actions: read

jobs:
  trivy-scan:
    name: Trivy Security Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t cinema-app:${{ github.sha }} .

      # Scan và in kết quả dạng bảng (không fail)
      - name: Run Trivy scan (table — xem chi tiết trong log)
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: cinema-app:${{ github.sha }}
          format: table
          severity: CRITICAL,HIGH
          exit-code: 0

      # Scan SARIF và FAIL nếu có CRITICAL
      - name: Run Trivy vulnerability scanner (SARIF)
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: cinema-app:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH
          exit-code: 1          # ← FAIL pipeline nếu có CRITICAL

      - name: Upload results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v4
        if: always()
        continue-on-error: true
        with:
          sarif_file: trivy-results.sarif

  docker-build-test:
    name: Docker Build & Smoke Test
    runs-on: ubuntu-latest
    needs: trivy-scan          # ← Chỉ chạy nếu trivy-scan PASS

    steps:
      - name: Checkout source code
        uses: actions/checkout@v4

      - name: Start services with Docker Compose
        run: docker compose up -d --build

      - name: Wait for services
        run: sleep 30 && docker compose ps

      - name: Smoke test — check HTTP 200
        run: |
          STATUS=$(curl -o /dev/null -s -w "%{http_code}" http://localhost:80)
          [ "$STATUS" = "200" ] && echo "✅ OK" || exit 1

      - name: Tear down
        if: always()
        run: docker compose down -v
```

## 2.3 Nguyên tắc FAIL/PASS

```
Có CVE CRITICAL? ──► YES ──► Pipeline FAIL ──► Không deploy
                 │
                 └─► NO  ──► Pipeline PASS ──► Deploy tiếp tục
```

### Tại sao FAIL là đúng?

> Trong DevSecOps, pipeline **cố tình FAIL** khi phát hiện lỗ hổng nghiêm trọng.  
> Đây là cơ chế **"Shift-left Security"** — phát hiện sớm trước khi lên production.  
> Nếu để pipeline luôn PASS, bảo mật trở thành vô nghĩa.

## 2.4 Kết quả thực tế

| Run | Commit | Kết quả | Lý do |
|---|---|---|---|
| #1 | `74cd7b3` | ❌ FAIL | Thiếu permissions |
| #2 | `f112f5c` | ❌ FAIL | Trivy tìm thấy CRITICAL |
| #3 | `056d2ca` | ❌ FAIL | Trivy CRITICAL + warning deprecation |
| #4 | `439aff2` | ❌ FAIL | Trivy CRITICAL (đúng thiết kế) |

> **Kết luận:** Pipeline FAIL là **hoạt động đúng** — Trivy phát hiện 65 CVE  
> (11 CRITICAL, 54 HIGH) trong image `python:3.12-slim` và các thư viện.

## 2.5 Cách xem kết quả trên GitHub

1. Vào repository → tab **Actions**
2. Click vào run mới nhất
3. Click **Trivy Security Scan** → xem log bảng CVE
4. Vào tab **Security** → **Code scanning** để xem SARIF

## 2.6 Checklist Phần 2

- [x] `security.yml` đã tạo và push lên GitHub
- [x] Workflow trigger khi push vào `main`
- [x] Trivy scan tích hợp (format table + SARIF)
- [x] Pipeline FAIL khi có CRITICAL CVE
- [x] Job 2 phụ thuộc Job 1 (`needs: trivy-scan`)
- [x] Permissions đúng (`security-events: write`)
- [x] codeql-action nâng lên v4 (không deprecated)
