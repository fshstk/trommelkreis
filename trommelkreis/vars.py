from . import app
from .archive import SessionCollection

# TODO: find a way to maybe dynamically update this when file system changes?
sessions = SessionCollection()

@app.context_processor
def global_vars():
    return {}