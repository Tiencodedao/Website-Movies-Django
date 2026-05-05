#!/bin/sh
# entrypoint.sh — Script khởi động container Django
# Chạy trước gunicorn để đảm bảo mọi thứ sẵn sàng

set -e   # Dừng ngay nếu có lỗi

echo "=============================="
echo "  Cinema Django — Starting"
echo "=============================="

# Bước 1: Chờ MySQL sẵn sàng (phòng ngừa lỗi connection refused)
echo "[1/3] Waiting for database..."
python -c "
import time, sys
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_django.settings')
django.setup()
from django.db import connections
from django.db.utils import OperationalError
retries = 0
while retries < 30:
    try:
        connections['default'].ensure_connection()
        print('Database is ready!')
        break
    except OperationalError:
        retries += 1
        print(f'Retry {retries}/30...')
        time.sleep(2)
else:
    print('ERROR: Cannot connect to database!')
    sys.exit(1)
"

# Bước 2: Chạy migrations (nếu cần)
echo "[2/3] Running migrations..."
python manage.py migrate --noinput

# Bước 3: Khởi động Gunicorn
echo "[3/3] Starting Gunicorn..."
exec gunicorn cinema_django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
