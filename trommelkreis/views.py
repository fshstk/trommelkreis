from flask import render_template, abort, request, send_from_directory, send_file
import os
from datetime import datetime
from zipfile import ZipFile
import io

# from werkzeug import FileWrapper

from . import app
from .vars import sessions

################################################################################


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.jinja")


@app.route("/info")
def info():
    return render_template("info.jinja")


@app.route("/archiv")
@app.route("/archiv/")
def archive():
    return render_template(
        "archive.jinja", archive=sessions.grouped_by_month
    )  # TODO: old method


@app.route("/abo")
def subscribe():
    return render_template("subscribe.jinja")


@app.route("/challenge")
def challenge():
    return render_template("challenge.jinja")


################################################################################

# single session:
@app.route("/archiv/<int:number>")
def session(number):
    session = sessions.get_session_by_yyyymmdd(number)  # TODO: old method
    if session is not None:
        return render_template("session.jinja", session=session)
    else:
        return abort(400)


# entire session as zip file:
@app.route("/archiv/<int:number>.zip")
# @app.route('/archiv/<int:number>/download/<whatever>') # (debug) chrome likes to cache downloads
def download_session(number, whatever):
    session = sessions.get_session_by_yyyymmdd(number)  # TODO: old method
    if session is not None:
        data = io.BytesIO()
        with ZipFile(data, "w") as zipfile:
            for file in session.files:
                zipfile.write(
                    file.path, os.path.basename(file.path)
                )  # TODO: old method
        data.seek(0)
        return send_file(
            data,
            mimetype="application/zip",
            as_attachment=True,
            attachment_filename=str(number) + ".zip",
        )
    else:
        return abort(400)


# single mp3 from session:
@app.route("/archiv/<int:number>/<filename>")
def download_file(number, filename):
    session = sessions.get_session_by_yyyymmdd(number)  # TODO: old method
    if session is not None:
        file = session.get_file_by_name(filename)  # TODO: old method
        if file is not None:
            return send_file(file.path)
        else:
            return abort(400)
    else:
        return abort(400)


################################################################################

from .archive import Session

today = Session("20200401")  # TODO: old method
# today = None


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # try:
    #     today = sessions.get_session_by_yyyymmdd(datetime.today())  # TODO: old method
    # except:
    #     today = None

    if today is not None:
        if request.method == "POST":
            # save uploaded file here...
            return render_template("home.jinja")
        else:
            return render_template("upload.jinja", today=today)
    else:
        return render_template("nexttime.jinja")


################################################################################


@app.errorhandler(400)
@app.errorhandler(404)
def notfound(error):
    return render_template("error.jinja")


################################################################################


@app.route("/testfile")
def testfile():
    return send_from_directory(app.config["ARCHIVE_PATH"], "test.mp3")


@app.route("/test")
def testpage():
    return render_template("test.jinja")
