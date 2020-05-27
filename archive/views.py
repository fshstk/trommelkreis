from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from math import ceil
from datetime import datetime
from zipfile import ZipFile
import io

from archive.models import Challenge, Artist, Session


# Archive views:


def index(request):
    return redirect("archive:sessions")


def show_all_sessions(request):
    archive = [split_list_in_half(month) for month in Session.grouped_by_month()]
    archive.reverse()  # Reverse chronoloical order
    context = {"archive": archive}  # "archive": sessions.group_by_month
    return render(request, "archive/all_sessions.html", context)


@never_cache
def download_session(request, session):
    """Get all session files as zip archive."""
    session = get_object_or_404(Session, slug=session)
    # files = [file.filepath for file in session.files]
    archivename = "{}.zip".format(session)
    zipfile = compress_files(session.files, archivename)

    response = HttpResponse(zipfile, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format(archivename)
    return response


def show_single_session_if_no_copyright(request, session):
    session = get_object_or_404(Session, slug=session)
    if not session.copyright_issues:
        return show_single_session(request, session)
    else:
        context = {"session": session}
        return render(request, "archive/cannot_show.html", context)


def show_single_session(request, session):
    session = get_object_or_404(Session, slug=session)
    files = session.files_by_subsection
    context = {"session": session, "files": files}
    return render(request, "archive/session.html", context)


def show_all_artists(request):
    artists = Artist.objects.all()
    context = {"artists": artists}
    pass


def show_single_artist(request, artist):
    artist = get_object_or_404(Artist, slug=artist)
    context = {"artist": artist, "files": artist.audiofile_set.all()}
    return render(request, "archive/artist.html", context)


# def show_all_challenges(request):
#     challenges = Challenge.objects.all()
#     context = {"challenges": challenges}
#     pass


# def show_single_challenge(request, challenge):
#     challenge = get_object_or_404(Challenge, slug=challenge)
#     context = {"challenge": challenge, "files": challenge.audiofile_set.all()}
#     return render(request, "archive/challenge.html", context)


# Helper functions:


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
