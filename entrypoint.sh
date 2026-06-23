#!/bin/sh
# entrypoint.sh — Cloud Run compatible (no blocking waits)

echo "=============================="
echo "  Cinema Django — Starting"
echo "=============================="

# Chạy migrate (nếu lỗi DB chưa sẵn sàng thì bỏ qua, không dừng)
echo "[1/2] Running migrations (non-fatal)..."
python manage.py migrate --noinput 2>&1 || echo "[WARN] Migration failed - DB may not be ready yet"

# Khởi động Gunicorn ngay lập tức (Cloud Run cần port mở sớm)
echo "[2/2] Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn cinema_django.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
