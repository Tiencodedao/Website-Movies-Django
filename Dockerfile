FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cài dependencies hệ thống cho mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Bảo mật: tạo non-root user để chạy ứng dụng
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Build static files (cần SECRET_KEY placeholder)
ENV SECRET_KEY=build-time-placeholder-not-used-in-production
ENV DEBUG=False
ENV ALLOWED_HOSTS=*
RUN python manage.py collectstatic --noinput

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Trao quyền sở hữu thư mục app cho non-root user
RUN chown -R appuser:appgroup /app

# Chuyển sang non-root user (bảo mật runtime)
USER appuser

# Cloud Run / Docker Compose dùng port 8000
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
