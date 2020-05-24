from trommelkreis.settings.common import *

SECRET_KEY = get_secret("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "trommelkreis.club",
    "www.trommelkreis.club",
    "localhost",
    "192.168.178.*",
]

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "trommelkreis_test",
        "USER": "trommelkreis",
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": "data.trommelkreis.club",
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    },
    # "archive": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "trommelkreis_archive",
    #     "USER": "trommelkreis",
    #     "PASSWORD": get_secret("DB_PASSWORD"),
    #     "HOST": "data.trommelkreis.club",
    #     "PORT": "3306",
    #     "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    # },
}
