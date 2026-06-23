import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-cinema-key-12345')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS_ENV = os.getenv('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_ENV.split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',   # ← CORS cho Mobile API
    'movies',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # ← Phải đặt đầu tiên
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinema_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cinema_django.wsgi.application'

# Cloud SQL: tách thành 3 biến để tránh lỗi parse dấu ':' trong --set-env-vars
_SQL_PROJECT = os.getenv('CLOUD_SQL_PROJECT', '')
_SQL_REGION = os.getenv('CLOUD_SQL_REGION', 'asia-southeast1')
_SQL_INSTANCE = os.getenv('CLOUD_SQL_INSTANCE', '')

if _SQL_PROJECT and _SQL_INSTANCE:
    # Kết nối Cloud SQL qua Unix socket (Cloud Run)
    _SOCKET_PATH = f'/cloudsql/{_SQL_PROJECT}:{_SQL_REGION}:{_SQL_INSTANCE}'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'cinema'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
            'HOST': 'localhost',
            'PORT': '',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'unix_socket': _SOCKET_PATH,
            },
        }
    }
else:
    # Kết nối MySQL TCP thông thường (local dev / Docker)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'cinema'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
SESSION_COOKIE_AGE = 86400  # 1 ngày

# Cloud Run: HTTPS được xử lý bởi load balancer, cần khai báo trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.run.app',
    'https://cinema-app-167139522127.asia-southeast1.run.app',
    'http://localhost',
    'http://127.0.0.1',
]

# Cloud Run proxy SSL header — để Django nhận biết đang chạy qua HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ────────────────────────────────────────────────────────────────
# CORS — Cho phép Flutter Mobile App gọi API
# ────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS  = True          # Development: cho phép mọi origin
# Production: đổi thành False và chỉ định domain cụ thể:
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',            # Flutter web dev
#     'https://your-app.run.app',        # Cloud Run
# ]
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization',
    'content-type', 'origin', 'x-requested-with',
]
