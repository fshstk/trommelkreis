from trommelkreis.settings.common import *

SECRET_KEY = get_secret("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    "trommelkreis.club",
    "www.trommelkreis.club",
    "localhost",
    "192.168.178.*",
]

# Database

DATABASES = {
    # Local development DB:
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "trommelkreis_dev",
        "USER": "root",
        "PASSWORD": get_secret("DEV_DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    },
    # TEST DATABASE:
    # "test_archive": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "trommelkreis_test",
    #     "USER": "trommelkreis",
    #     "PASSWORD": get_secret("DB_PASSWORD"),
    #     "HOST": "data.trommelkreis.club",
    #     "PORT": "3306",
    #     "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    # },
}
