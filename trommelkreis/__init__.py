from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import locale

# from .archive import SessionCollection

locale.setlocale(locale.LC_ALL, "de_AT.UTF-8")
app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

from . import views
from .vars import *
