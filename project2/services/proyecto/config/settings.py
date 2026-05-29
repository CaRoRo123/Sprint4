from decouple import config
import dj_database_url

SECRET_KEY  = config("SECRET_KEY")
DEBUG       = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF      = "config.urls"
WSGI_APPLICATION  = "config.wsgi.application"

# ── Aurora PostgreSQL (write side) ───────────────────────────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=config("DB_SSL", default=False, cast=bool),
    )
}

# ── ElastiCache Redis ─────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# ── DynamoDB (read side) ──────────────────────────────────────────────────────
DYNAMODB_TABLE   = config("DYNAMODB_TABLE")
AWS_REGION       = config("AWS_REGION", default="us-east-1")

# ── REST Framework ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES":   ["rest_framework.parsers.JSONParser"],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE      = "es-co"
TIME_ZONE          = "America/Bogota"
USE_TZ             = True
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Si no hay DB_HOST en el .env, usamos sqlite3 localmente
if not os.getenv("DB_HOST"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Tu configuración actual de PostgreSQL
    pass