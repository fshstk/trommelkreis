from flask import render_template, abort, request, send_from_directory
import os

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

@app.route('/abo')
def subscribe():
    return render_template('subscribe.jinja')

@app.route('/challenge')
def challenge():
    return render_template('challenge.jinja')

################################################################################

@app.route('/archiv/<int:number>')
def session(number):
    session = sessions.get_session_by_yyyymmdd(number)
    if session is not None:
        return render_template('session.jinja', session = session)
    else:
        return abort(400)

@app.route('/archiv/<int:number>.zip')
def download_session(number):
    session = sessions.get_session_by_yyyymmdd(number)
    if session is not None:
        # serve zip file here...
        return render_template('home.jinja')
    else:
        return abort(400)

@app.route('/archiv/<int:number>/<filename>')
def download_file(number, filename):
    session = sessions.get_session_by_yyyymmdd(number)
    if session is not None:
        file = session.get_file_by_name(filename)
        if file is not None:
            # serve mp3/wav here...
            return render_template('home.jinja')
        else:
            return abort(400)
    else:
        return abort(400)

################################################################################

from .archive import Session
today = Session("20200401")
# today = None

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if today is not None:
        if request.method == "POST":
            # save uploaded file here...
            return render_template('home.jinja')
        else:
            return render_template('upload.jinja', today = today)
    else:
        return render_template('nexttime.jinja')

################################################################################

@app.errorhandler(400)
@app.errorhandler(404)
def notfound(error):
    return render_template('error.jinja')

################################################################################

@app.route('/testfile')
def testfile():
    return send_from_directory(app.config["ARCHIVE_PATH"], 'test.mp3')

@app.route('/test')
def testpage():
    return render_template('test.jinja')