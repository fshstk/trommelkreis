from flask import render_template, abort, request, send_file
import os
from datetime import datetime
from zipfile import ZipFile
import io
from sqlalchemy.orm.exc import NoResultFound
from . import app
from .archive import Session, AudioFile, Challenge


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
    return render_template("archive.jinja", archive=Session.grouped_by_month())


@app.route("/abo")
def subscribe():
    return render_template("subscribe.jinja")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    try:
        today = Session.query.filter_by(date=datetime.today())
    except NoResultFound:
        return render_template("nexttime.jinja")

    if request.method == "POST":
        # save uploaded file here...
        return render_template("home.jinja")
    else:
        return render_template("upload.jinja", today=today)


################################################################################


# Show single session:
@app.route("/archiv/<name>")
def get_session(name):
    try:
        session = Session.from_name(name)
    except NoResultFound:
        return abort(400)
    return render_template("session.jinja", session=session)


# Get all session files as zip archive:
@app.route("/archiv/<name>.zip")
def download_session(name):
    try:
        session = Session.from_name(name)
    except NoResultFound:
        return abort(400)
    return send_files_as_zip(session.files, name=name)


# Get single MP3 from session:
@app.route("/archiv/<name>/<filename>")
def download_file(name, filename):
    try:
        session = Session.from_name(name)
    except NoResultFound:
        return abort(400)

    try:
        file = session.get_file_by_name(filename)
    except NoResultFound:
        return abort(400)

    return send_file(
        io.BytesIO(file.data),
        mimetype="audio/mpeg",  # TODO: remove if using types other than mp3 files
        as_attachment=True,
        attachment_filename=file.filename,
    )


################################################################################


def send_files_as_zip(filelist, name):
    zipdata = io.BytesIO()
    with ZipFile(zipdata, "w") as zipfile:
        for file in filelist:
            zipfile.writestr(file.filename, file.data)
    zipdata.seek(0)
    return send_file(
        zipdata,
        mimetype="application/zip",
        as_attachment=True,
        attachment_filename="{}.zip".format(name),
    )


################################################################################


@app.errorhandler(400)
@app.errorhandler(404)
def notfound(error):
    return render_template("error.jinja")
