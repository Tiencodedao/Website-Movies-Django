# Phần 3 — Google Cloud VM & Triển khai

## 3.1 Thông tin VM

| Thuộc tính | Giá trị |
|---|---|
| Tên VM | `cinema-devsecops-vm` |
| Project | `cinema-django-app` |
| Zone | `asia-southeast1-b` (Singapore) |
| Machine type | `e2-medium` (2 vCPU, 4 GB RAM) |
| OS | Ubuntu 22.04 LTS |
| Disk | 20 GB SSD |
| External IP | `35.240.177.27` |
| Docker version | 29.6.0 |
| Docker Compose | v5.1.4 |

## 3.2 Tạo VM bằng gcloud SDK

### Cài gcloud và đăng nhập
```powershell
# Đăng nhập
gcloud auth login

# Xem Project ID thực tế
gcloud projects list

# Set đúng Project ID
gcloud config set project cinema-django-app   # ← Dùng PROJECT_ID, không phải tên

# Bật Compute Engine API
gcloud services enable compute.googleapis.com
```

### Tạo VM
```powershell
gcloud compute instances create cinema-devsecops-vm `
  --zone=asia-southeast1-b `
  --machine-type=e2-medium `
  --image-family=ubuntu-2204-lts `
  --image-project=ubuntu-os-cloud `
  --boot-disk-size=20GB `
  --boot-disk-type=pd-balanced `
  --tags=http-server
```

### Mở firewall
```powershell
# Port 80 (website)
gcloud compute firewall-rules create allow-http-80 `
  --allow=tcp:80 `
  --source-ranges=0.0.0.0/0

# Port 8080 (phpMyAdmin)
gcloud compute firewall-rules create allow-port-8080 `
  --allow=tcp:8080 `
  --source-ranges=0.0.0.0/0
```

### SSH vào VM
```powershell
gcloud compute ssh cinema-devsecops-vm --zone=asia-southeast1-b
```

## 3.3 Cài Docker trên VM

```bash
# Script cài Docker CE chính thức (trong SSH terminal)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# Kiểm tra
docker --version          # Docker version 29.6.0
docker compose version    # Docker Compose version v5.1.4
```

## 3.4 Clone và cấu hình dự án

```bash
# Cài git
sudo apt install git -y

# Clone từ GitHub
git clone https://github.com/Tiencodedao/Website-Movies-Django.git
cd Website-Movies-Django

# Tạo file .env.docker (phải tạo thủ công vì gitignore)
cat > .env.docker << 'EOF'
SECRET_KEY=cinema-devsecops-secret-key-2024
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
EOF
```

## 3.5 Lỗi thường gặp và cách sửa

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| `projects/X was not found` | Dùng Project Name thay vì Project ID | `gcloud projects list` → lấy đúng PROJECT_ID |
| `Invalid value for field 'resource.tags'` | Dấu phẩy trong PowerShell | Dùng `--tags=http-server --tags=https-server` (tách riêng) |
| `docker-compose-plugin not found` | Ubuntu repo mặc định không có | Dùng `curl -fsSL https://get.docker.com \| sudo sh` |
| Website không load từ ngoài | Firewall chưa mở port 80 | Tạo firewall rule `allow-http-80` (không target tag) |
| phpMyAdmin timeout | Firewall rule có `target-tags` nhưng VM không có tag đó | Tạo rule không có target-tags |

## 3.6 Checklist Phần 3

- [x] VM tạo thành công (`cinema-devsecops-vm`)
- [x] Firewall port 80 mở (toàn bộ internet)
- [x] Firewall port 8080 mở (toàn bộ internet)
- [x] Docker CE 29.6.0 đã cài
- [x] Docker Compose v5.1.4 đã cài
- [x] Git clone thành công
- [x] `.env.docker` đã tạo với IP đúng
