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


def sessions(request):
    # Remove empty sessions (no files) so they don't get displayed:
    # (This is a bit confusing because of the nested array.)
    archive = [
        [session for session in month if len(session.files) > 0]
        for month in Session.grouped_by_month()
    ]
    # Remove empty months and split into halves:
    archive = [split_list_in_half(month) for month in archive if len(month) > 0]
    archive.reverse()  # Reverse chronoloical order
    context = {"archive": archive}  # "archive": sessions.group_by_month
    return render(request, "archive/sessions_all.html", context)


# @never_cache
# def download_session(request, session):
#     """Get all session files as zip archive."""
#     session = get_object_or_404(Session, slug=session)
#     # files = [file.filepath for file in session.files]
#     archivename = "{}.zip".format(session)
#     zipfile = compress_files(session.files, archivename)

#     response = HttpResponse(zipfile, content_type="application/zip")
#     response["Content-Disposition"] = "attachment; filename={}".format(archivename)
#     return response


def single_session_if_no_copyright(request, session):
    session = get_object_or_404(Session, slug=session)
    if not session.copyright_issues:
        return single_session_unconditional(request, session)
    else:
        context = {"session": session}
        return render(request, "archive/cannot_show.html", context)


def single_session_unconditional(request, session):
    session = get_object_or_404(Session, slug=session)
    files = session.files_by_subsection
    context = {"session": session, "files": files}
    return render(request, "archive/sessions_single.html", context)


def artists(request):
    artists = Artist.objects.order_by("name")
    context = {"artists": artists}
    return render(request, "archive/artists_all.html", context)


def single_artist(request, artist):
    artist = get_object_or_404(Artist, slug=artist)
    context = {"artist": artist, "files": artist.tracks.all()}
    return render(request, "archive/artists_single.html", context)


# def challenges(request):
#     challenges = Challenge.objects.all()
#     context = {"challenges": challenges}
#     pass


# def single_challenge(request, challenge):
#     challenge = get_object_or_404(Challenge, slug=challenge)
#     context = {"challenge": challenge, "files": challenge.tracks.all()}
#     return render(request, "archive/challenges_single.html", context)


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


# def compress_files(filelist, archivename):
#     """Takes in a list of AudioFile objects and archive name, and returns ZIP file as BytesIO object."""
#     zipdata = io.BytesIO()
#     with ZipFile(zipdata, "w") as zipfile:
#         for file in filelist:
#             zipfile.writestr(file.filename, file.data.read())
#     zipdata.seek(0)
#     return zipdata
