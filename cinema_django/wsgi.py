"""
WSGI config for cinema_django project.
Uses WhiteNoise WSGI wrapper to serve static files in production (Cloud Run).
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_django.settings')

application = get_wsgi_application()

# Wrap with WhiteNoise to serve static files without a separate web server
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'staticfiles'

application = WhiteNoise(application, root=str(STATIC_ROOT), prefix='static')
