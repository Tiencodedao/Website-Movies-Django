# Hướng dẫn chạy project với Docker - Chi tiết từng bước

## Bước 1: Cài đặt Docker Desktop

### Windows:
1. Tải Docker Desktop từ: https://www.docker.com/products/docker-desktop/
2. Chạy file cài đặt và làm theo hướng dẫn
3. Khởi động lại máy tính sau khi cài đặt
4. Mở Docker Desktop và đợi cho đến khi nó chạy (biểu tượng Docker ở system tray không còn nhấp nháy)

### Kiểm tra Docker đã cài đặt thành công:
```bash
# Mở Command Prompt hoặc PowerShell và chạy:
docker --version
docker-compose --version
```

Kết quả mong đợi:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

## Bước 2: Chuẩn bị project

### 2.1 Kiểm tra cấu trúc thư mục
Đảm bảo bạn có các file sau trong thư mục `d:\MOVIE WEBSITES`:
```
d:\MOVIE WEBSITES\
├── config\
│   └── config.php
├── cinema.sql
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
└── (các file PHP khác của bạn)
```

### 2.2 Kiểm tra file cinema.sql
- Đảm bảo file `cinema.sql` nằm ở thư mục gốc `d:\MOVIE WEBSITES\`
- File này sẽ tự động import database khi khởi động lần đầu

## Bước 3: Chạy Docker Containers

### 3.1 Mở Terminal
**Windows Command Prompt:**
```cmd
cd /d "d:\MOVIE WEBSITES"
```

**Windows PowerShell:**
```powershell
cd "d:\MOVIE WEBSITES"
```

**Git Bash:**
```bash
cd /d/MOVIE\ WEBSITES
```

### 3.2 Khởi động containers lần đầu
```bash
docker-compose up -d
```

**Giải thích:**
- `docker-compose up`: Tạo và khởi động tất cả containers
- `-d`: Chạy ở chế độ background (detached mode)

**Quá trình sẽ diễn ra:**
1. Download các Docker images (MySQL, PHP, phpMyAdmin) - lần đầu mất 5-10 phút
2. Tạo network và volumes
3. Khởi động MySQL container
4. Build PHP container
5. Import database từ cinema.sql
6. Khởi động phpMyAdmin

### 3.3 Xem quá trình khởi động
```bash
docker-compose logs -f
```

**Thoát xem logs:** Nhấn `Ctrl + C`

### 3.4 Kiểm tra containers đang chạy
```bash
docker-compose ps
```

Kết quả mong đợi:
```
NAME                 IMAGE              STATUS          PORTS
cinema_db            mysql:8.0          Up 2 minutes    0.0.0.0:3306->3306/tcp
cinema_web           movie-web:latest   Up 2 minutes    0.0.0.0:8080->80/tcp
cinema_phpmyadmin    phpmyadmin:latest  Up 2 minutes    0.0.0.0:8081->80/tcp
```

## Bước 4: Truy cập ứng dụng

### 4.1 Truy cập Website
- Mở trình duyệt và vào: **http://localhost:8080**
- Hoặc: **http://127.0.0.1:8080**

### 4.2 Truy cập phpMyAdmin
- URL: **http://localhost:8081**
- **Server:** db
- **Username:** root
- **Password:** root_password

**Hoặc đăng nhập với user thường:**
- **Username:** cinema_user
- **Password:** cinema_pass

### 4.3 Kết nối MySQL từ máy local (nếu cần)
```
Host: localhost
Port: 3306
Database: cinema
Username: cinema_user
Password: cinema_pass
```

## Bước 5: Các lệnh thường dùng

### Xem logs của tất cả containers
```bash
docker-compose logs -f
```

### Xem logs của container cụ thể
```bash
# Logs của PHP web
docker-compose logs -f web

# Logs của MySQL
docker-compose logs -f db

# Logs của phpMyAdmin
docker-compose logs -f phpmyadmin
```

### Dừng containers (nhưng giữ lại data)
```bash
docker-compose stop
```

### Khởi động lại containers đã dừng
```bash
docker-compose start
```

### Dừng và xóa containers (giữ lại data)
```bash
docker-compose down
```

### Khởi động lại containers
```bash
docker-compose restart
```

### Dừng, xóa containers VÀ xóa database
```bash
docker-compose down -v
```
**⚠️ Cảnh báo:** Lệnh này sẽ xóa toàn bộ database!

### Rebuild containers (khi thay đổi Dockerfile)
```bash
docker-compose up -d --build
```

### Vào bên trong container để chạy lệnh
```bash
# Vào PHP container
docker exec -it cinema_web bash

# Vào MySQL container
docker exec -it cinema_db bash

# Thoát khỏi container
exit
```

## Bước 6: Khắc phục sự cố

### Lỗi: Port đã được sử dụng
```
Error: Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Giải pháp:**
1. Đổi port trong `docker-compose.yml`:
```yaml
web:
  ports:
    - "8888:80"  # Thay vì 8080
```

2. Hoặc tắt ứng dụng đang dùng port đó

### Lỗi: Database không import được
**Kiểm tra logs:**
```bash
docker-compose logs db
```

**Reset và import lại:**
```bash
docker-compose down -v
docker-compose up -d
```

### Lỗi: Không kết nối được database từ PHP
**Kiểm tra:**
1. Container db đã chạy chưa: `docker-compose ps`
2. Đợi 30 giây để MySQL khởi động hoàn toàn
3. Xem logs: `docker-compose logs db`

**Test kết nối:**
```bash
docker exec -it cinema_web php -r "echo 'Test connection';"
```

### Website bị lỗi 403 Forbidden
**Kiểm tra permissions:**
```bash
docker exec -it cinema_web bash
ls -la /var/www/html
```

**Fix permissions:**
```bash
docker exec -it cinema_web chown -R www-data:www-data /var/www/html
docker exec -it cinema_web chmod -R 755 /var/www/html
```

### Xóa toàn bộ và bắt đầu lại từ đầu
```bash
# Dừng và xóa tất cả
docker-compose down -v

# Xóa images (nếu cần)
docker-compose down --rmi all

# Khởi động lại
docker-compose up -d
```

## Bước 7: Làm việc với code

### Chỉnh sửa code PHP
1. Mở file PHP bình thường với editor (VS Code, Notepad++, v.v.)
2. Lưu file
3. **Không cần restart container** - thay đổi sẽ tự động có hiệu lực
4. Refresh trình duyệt để thấy thay đổi

### Thêm PHP extension mới
1. Sửa file `Dockerfile`
2. Rebuild container:
```bash
docker-compose up -d --build
```

### Thay đổi cấu hình MySQL
1. Sửa file `docker-compose.yml` phần `db`
2. Restart:
```bash
docker-compose restart db
```

## Bước 8: Backup và Restore

### Backup database
```bash
docker exec cinema_db mysqldump -u root -proot_password cinema > backup_$(date +%Y%m%d).sql
```

### Restore database
```bash
docker exec -i cinema_db mysql -u root -proot_password cinema < backup_20250504.sql
```

## Thông tin cấu hình

### Ports
- **8080**: Website PHP
- **8081**: phpMyAdmin
- **3306**: MySQL database

### Credentials
**MySQL Root:**
- Username: root
- Password: root_password

**MySQL User:**
- Username: cinema_user
- Password: cinema_pass
- Database: cinema

### Volumes
- `db_data`: Lưu trữ MySQL data (persistent)

### Networks
- `cinema_network`: Network nội bộ giữa các containers

## Lưu ý quan trọng

1. **Lần chạy đầu tiên** sẽ mất thời gian để download images (~500MB-1GB)
2. **Database tự động import** từ file `cinema.sql` khi khởi động lần đầu
3. **Dữ liệu được lưu trữ** trong Docker volume, không bị mất khi restart
4. **Code thay đổi tự động** - không cần rebuild container khi sửa PHP
5. **Để xóa hoàn toàn** dùng: `docker-compose down -v`

## Hỗ trợ

Nếu gặp vấn đề, kiểm tra logs:
```bash
docker-compose logs -f
```

Hoặc vào container để debug:
```bash
docker exec -it cinema_web bash
docker exec -it cinema_db bash
```
