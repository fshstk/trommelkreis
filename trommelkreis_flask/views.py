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
    archive = Session.grouped_by_month()
    archive.reverse()  # Display in reverse chronological order
    return render_template("archive.jinja", archive=archive)


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
@app.route("/archiv/<session>")
def get_session(session):
    try:
        session = Session.from_slug(session)
    except NoResultFound:
        return abort(400)
    return render_template("session.jinja", session=session)


# Get all session files as zip archive:
@app.route("/archiv/<session>.zip")
def download_session(session):
    try:
        session = Session.from_slug(session)
    except NoResultFound:
        return abort(400)
    return send_files_as_zip(session.files, archivename=session)


# Get single MP3 from session:
@app.route("/archiv/<session>/<file>")
def download_file(session, file):
    try:
        session = Session.from_slug(session)
    except NoResultFound:
        return abort(400)

    try:
        track = session.get_file_by_slug(file)
    except NoResultFound:
        return abort(400)

    return send_file(
        io.BytesIO(track.data),
        mimetype="audio/mpeg",
        as_attachment=True,
        attachment_filename=track.filename,
    )


################################################################################


def send_files_as_zip(filelist, archivename):
    zipdata = io.BytesIO()
    with ZipFile(zipdata, "w") as zipfile:
        for file in filelist:
            zipfile.writestr(file.filename, file.data)
    zipdata.seek(0)
    return send_file(
        zipdata,
        mimetype="application/zip",
        as_attachment=True,
        attachment_filename="{}.zip".format(archivename),
    )


################################################################################


@app.errorhandler(400)
@app.errorhandler(404)
def notfound(error):
    return render_template("error.jinja")
