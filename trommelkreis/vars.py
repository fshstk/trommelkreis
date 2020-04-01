from . import app
from .archive import SessionCollection

sessions = SessionCollection()

@app.context_processor
def global_vars():
    return {}