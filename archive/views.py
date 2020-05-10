from django.shortcuts import render, get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse, HttpResponseRedirect

from math import ceil
from datetime import datetime
from zipfile import ZipFile
import io

from archive.models import Session
from archive.forms import UploadForm


def show_all_sessions(request):
    archive = [split_list_in_half(month) for month in Session.grouped_by_month()]
    archive.reverse()  # Reverse chronoloical order
    context = {"archive": archive}  # "archive": sessions.group_by_month
    return render(request, "archive/all_sessions.html", context)


def download_session(request, session):
    """Get all session files as zip archive."""
    session = get_session_from_slug(session)
    # files = [file.filepath for file in session.files]
    archivename = "{}.zip".format(session)
    zipfile = compress_files(session.files, archivename)

    response = HttpResponse(zipfile, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format(archivename)
    return response


def show_single_session(request, session):
    session = get_session_from_slug(session)
    context = {"session": session}
    return render(request, "archive/session.html", context)


def upload_form(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: form parsing
            # TODO: make this page, or do it spa style in JS, OR use url name or whatever
            return HttpResponseRedirect("/archive/<session>")
    else:
        form = UploadForm()

    return render(request, "upload.html", {"form": form})


# Helper functions:


def get_session_from_slug(slug):
    """Get session with date in yyyymmdd format, or raise 404 error if not found."""
    seshdate = datetime.strptime(slug, "%Y%m%d")
    session = get_object_or_404(Session, date=seshdate)
    return session


def split_list_in_half(list):
    """
    Splits a list into two equally sized sublists,
    with the first being one larger if len(list) is odd.
    """
    middle_index = ceil(len(list) / 2)
    first_half = list[:middle_index]
    second_half = list[middle_index:]
    return [first_half, second_half]


def compress_files(filelist, archivename):
    """Takes in a list of AudioFile objects and archive name, and returns ZIP file as BytesIO object."""
    zipdata = io.BytesIO()
    with ZipFile(zipdata, "w") as zipfile:
        for file in filelist:
            zipfile.write(file.filepath, file.filename)
    zipdata.seek(0)
    return zipdata
