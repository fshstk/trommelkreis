"""
These are the Django settings for a Heroku/Dokku deployment.

The following env variables should be set:
SECRET_KEY:             [Unique secret key for Django app]
DATABASE_URL:           [mysql://db_user:db_password@db_host:db_port/db_name]
DEBUG:                  [Enable debug mode (1 or 0)]
DJANGO_SETTINGS_MODULE: trommelkreis.settings.heroku
MEDIA_ROOT:             [Place in file system where media files are stored.
                        Make sure that this is a mounted persistent storage
                        volume]
MEDIA_PASSWORD:         [URL Suffix for copyrighted sessions]
PREVIEW_PASSWORD:       [URL Suffix for previewing unpublished challenges]
WEB_CONCURRENCY:        [How many worker proceses to use (3)]
"""

import os
import django_heroku

# DEBUG is a string and could be "1", "true" or "True":
DEBUG = os.environ.get("DEBUG").lower() in ["1", "true"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
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

STATICFILES_DIRS = [os.path.join(BASE_DIR, "trommelkreis", "static")]
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)
LIBSASS_OUTPUT_STYLE = "nested" if DEBUG else "compressed"

# Compressed assets (CSS) will fail to be generated before running the server
# unless manage.py compress is run. The following line ensures that NOT running
# this command will result in a failed build (which is preferable to 404 errors
# that might go unnoticed):
COMPRESS_OFFLINE = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT")

# Password for unlocking copyrighted media:
MEDIA_PASSWORD = os.environ.get("MEDIA_PASSWORD")

# Password for previewing challenge before uploads are open:
PREVIEW_PASSWORD = os.environ.get("PREVIEW_PASSWORD")

# This line serves no purpose other than to calm down the Python linter during development...
DATABASES = {"default": None}

# A few default configs, including setting up static files and the database from DATABASE_URL:
django_heroku.settings(locals())

# The following line is required since dj_database_url sets the "sslmode=required" option, which
# throws an error with mysql databases:
del DATABASES["default"]["OPTIONS"]["sslmode"]

# Enable mysql strict mode (recommended for data integrity):
DATABASES["default"]["OPTIONS"].update(
    {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"}
)
