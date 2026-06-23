import os
os.environ.setdefault('SECRET_KEY', 'test-key-for-debug')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '*')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_django.settings')

import django
django.setup()

from django.conf import settings

print("=== WhiteNoise Debug ===")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATIC_ROOT exists: {settings.STATIC_ROOT.exists()}")

if settings.STATIC_ROOT.exists():
    files = list(settings.STATIC_ROOT.rglob('*'))
    print(f"Total files in STATIC_ROOT: {len([f for f in files if f.is_file()])}")

print("Middleware with whitenoise:")
for m in settings.MIDDLEWARE:
    if 'white' in m.lower():
        print(f"  -> {m}")
        
# Test whitenoise directly
from whitenoise import WhiteNoise
app = WhiteNoise(None, root=str(settings.STATIC_ROOT), prefix='static')
print(f"WhiteNoise loaded files: {len(app.files)}")
print("Sample files:")
for path in list(app.files.keys())[:5]:
    print(f"  {path}")
