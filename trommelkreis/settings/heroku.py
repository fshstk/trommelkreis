"""
Django settings for trommelkreis project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

DEBUG = bool(os.environ.get("DEBUG"))

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
