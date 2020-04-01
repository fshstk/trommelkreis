from flask import render_template, abort

from . import app
from .vars import sessions

################################################################################

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.jinja')

@app.route('/info')
def info():
    return render_template('info.jinja')

@app.route('/archiv')
@app.route('/archiv/')
def archive():
    return render_template('archive.jinja', archive = sessions.grouped_by_month)

@app.route('/upload')
def upload():
    return render_template('upload.jinja')

@app.route('/abo')
def subscribe():
    return render_template('subscribe.jinja')

@app.route('/challenge')
def challenge():
    return render_template('challenge.jinja')

@app.route('/archiv/<int:number>')
def session(number):
    session = sessions.get_session_by_yyyymmdd(number)
    if session is not None:
        return render_template('session.jinja', session = session)
    else:
        return abort(400)

################################################################################

@app.errorhandler(404) # possibly add more errors (403, 500)
def notfound(error):
    return render_template('error.jinja')

@app.errorhandler(400)
def badrequest(error):
    # return render_template('session_not_found.jinja', archive = sessions.grouped_by_month)
    return notfound(None)