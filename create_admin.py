"""
Script tạo CinemaUser admin — chạy trong Cloud Run job
Dùng CinemaUser model (bảng users) + bcrypt password
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_django.settings')
django.setup()

import bcrypt
from movies.models import CinemaUser

name     = os.getenv('ADMIN_NAME',     'Admin')
email    = os.getenv('ADMIN_EMAIL',    'admin@cinema.com')
password = os.getenv('ADMIN_PASSWORD', 'Admin@1234')

# Xóa nếu email đã tồn tại
deleted, _ = CinemaUser.objects.filter(user_email=email).delete()
if deleted:
    print(f"[INFO] Đã xóa CinemaUser cũ: {email}")

# Hash password bằng bcrypt (giống hệ thống)
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Tạo user mới
user = CinemaUser.objects.create(
    user_name=name,
    user_email=email,
    user_password=hashed,
    user_role='admin',
    IsStaff=True,
)

print(f"[OK] CinemaUser admin tạo thành công!")
print(f"     Name     : {user.user_name}")
print(f"     Email    : {user.user_email}")
print(f"     Role     : {user.user_role}")
print(f"     IsStaff  : {user.IsStaff}")
print(f"     Login tại: /login/")
