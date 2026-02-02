import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret-key")
DEBUG = False

ALLOWED_HOSTS = [
    '*', 
    'orthocare-backend-production.up.railway.app',
    'orthocare-backend-production.railway.app'
]

CSRF_TRUSTED_ORIGINS = [  # ← CRITICAL FOR HTTPS ADMIN LOGIN
    'https://orthocare-backend-production.up.railway.app',
    'https://orthocare-backend-production.railway.app'
]

CORS_ALLOWED_ORIGINS = [  # ← YOUR EXISTING CORS
    "http://localhost:8080",
    "http://localhost:5173", 
    "https://orthocare-backend-production.up.railway.app",
]


DATABASES = {
    "default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",           # ← ADD + TOP
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",       # ← AFTER CORS
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "project_name.urls"
WSGI_APPLICATION = "project_name.wsgi.application"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

print("✅ SETTINGS LOADED")
print("✅ DB URL =", os.environ.get("DATABASE_URL"))


DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"  # Already correct


import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'