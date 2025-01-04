"""
The following env variables should be set:
SECRET_KEY:             [Unique secret key for Django app]
DATABASE_URL:           [mysql://db_user:db_password@db_host:db_port/db_name]
DEBUG:                  [Enable debug mode (1 or 0)]
MEDIA_PASSWORD:         [URL Suffix for copyrighted sessions]
PREVIEW_PASSWORD:       [URL Suffix for previewing unpublished challenges]
"""

import os
import dj_database_url

DEBUG = os.environ.get("DEBUG", "0") == "1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "django_gulp",
    "archive",
    "uploadform.apps.UploadFormConfig",
    "pagedown.apps.PagedownConfig",
    "compressor",
    "django.contrib.admin",
    "solo.apps.SoloAppConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
]

GRAPHENE = {"SCHEMA": "archive.schema.schema"}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "trommelkreis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "trommelkreis", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "trommelkreis.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "de-at"
TIME_ZONE = "Europe/Vienna"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "trommelkreis", "static"),
    os.path.join(BASE_DIR, "_fonts"),
    os.path.join(BASE_DIR, "_scripts"),
]

STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Compressed assets (CSS) will fail to be generated before running the server
# unless manage.py compress is run. The following line ensures that NOT running
# this command will result in a failed build (which is preferable to 404 errors
# that might go unnoticed):
COMPRESS_OFFLINE = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
os.makedirs(STATIC_ROOT, exist_ok=True)

# Password for unlocking copyrighted media:
MEDIA_PASSWORD = os.environ.get("MEDIA_PASSWORD", "_")

# Password for previewing challenge before uploads are open:
PREVIEW_PASSWORD = os.environ.get("PREVIEW_PASSWORD", "_")

DATABASES = {"default": dj_database_url.config()}

SECRET_KEY = os.environ.get("SECRET_KEY", "_")

ALLOWED_HOSTS = [".localhost", "127.0.0.1", ".trommelkreis.club"]
CSRF_TRUSTED_ORIGINS = ["https://trommelkreis.club", "https://*.trommelkreis.club"]

AWS_S3_FILE_OVERWRITE = False

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "_")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "_")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "_")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "_")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
