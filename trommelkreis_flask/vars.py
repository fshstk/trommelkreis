from . import app


@app.context_processor
def global_vars():
    return {}
