# Docker Commands — Cinema Django
# Hướng dẫn build và chạy Docker cho đề tài báo cáo

## Yêu cầu
- Docker Desktop đang chạy

## Lệnh thực hiện (chạy trong terminal tại thư mục dự án)

### BUILD và RUN lần đầu
```
docker compose up --build
```

### Chạy lại (đã build rồi, không cần build lại)
```
docker compose up
```

### Dừng các container
```
docker compose down
```

### Xem trạng thái container
```
docker compose ps
```

### Xem log
```
docker compose logs web
docker compose logs db
```

### Xem danh sách image đã build
```
docker images
```

### Xem container đang chạy
```
docker ps
```

## Truy cập sau khi chạy
- Website:    http://localhost:8000
- phpMyAdmin: http://localhost:8080

## Thứ tự chạy (tự động)
1. Container `cinema_db` (MySQL) khởi động
2. Healthcheck kiểm tra MySQL sẵn sàng chưa
3. Container `cinema_web` (Django) start
4. entrypoint.sh: chờ DB → migrate → gunicorn
5. Website available tại http://localhost:8000
