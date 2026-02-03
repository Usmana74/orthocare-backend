import os
import dj_database_url
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    '*',
    'orthocare-backend-production.up.railway.app',
    'orthocare-backend-production.railway.app'
]

# 🔥 CSRF + CORS - RAILWAY HTTPS PRODUCTION
CSRF_TRUSTED_ORIGINS = [
    'https://orthocare-backend-production.up.railway.app',
    'https://orthocare-backend-production.railway.app',
    'http://orthocare-backend-production.up.railway.app',
    'http://orthocare-backend-production.railway.app'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "https://orthocare-backend-production.up.railway.app",
    "https://orthocare-backend-production.railway.app"
]

# APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "accounts",
    "patients",
    "visits",
]

# MIDDLEWARE - PERFECT ORDER
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "orthocare_backend.urls"  # ← FIXED project_name

# TEMPLATES
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = "orthocare_backend.wsgi.application"  # ← FIXED

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'vfElDzyslOQVwANnTHxFaJissuxqSUsT',
        'HOST': 'postgres.railway.internal',
        'PORT': '5432',
    }
}

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Karachi"
USE_I18N = True
USE_TZ = True

# STATIC + MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ADD THIS AT END OF settings.py (BEFORE print statements)
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orthocare_backend.settings')
django.setup()

if os.getenv('RUN_MIGRATIONS') == 'True':
    from django.core.management import call_command
    call_command('migrate', verbosity=2)
    print("✅ MIGRATIONS COMPLETE")

# Create superuser if doesn't exist
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@orthocare.com', 'orthocare123')
        print("✅ SUPERUSER CREATED: admin/orthocare123")
except:
    print("⚠️ Superuser creation skipped")

print("✅ SETTINGS LOADED SUCCESSFULLY")
print("✅ DATABASE:", DATABASES['default']['HOST'])
print("✅ CSRF_TRUSTED_ORIGINS:", len(CSRF_TRUSTED_ORIGINS), "origins")


print("✅ SETTINGS LOADED SUCCESSFULLY")
print("✅ CSRF_TRUSTED_ORIGINS:", len(CSRF_TRUSTED_ORIGINS), "origins")
