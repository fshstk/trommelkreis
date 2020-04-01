from flask import Flask
import locale

from .archive import SessionCollection

locale.setlocale(locale.LC_ALL, "de_AT.UTF-8")
app = Flask(__name__)
            
from . import views
from .vars import *