from django.shortcuts import render, get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear

from math import ceil

from archive.models import Session


def split_list_in_half(list):
    """
    Splits a list into two equally sized sublists,
    with the first being one larger if len(list) is odd.
    """
    middle_index = ceil(len(list) / 2)
    first_half = list[:middle_index]
    second_half = list[middle_index:]
    return [first_half, second_half]


def all_sessions(request):
    """Show list of all sessions."""
    archive = [split_list_in_half(month) for month in Session.grouped_by_month()]
    context = {"archive": archive}  # "archive": sessions.group_by_month
    return render(request, "archive/index.html", context)


def download_session(request, session):
    """Get all session files as zip archive."""
    try:
        pass  # look for session
    except Session.DoesNotExist:
        raise Http404("Session does not exist.")


def show_session(request, session):
    """Show single session."""
    try:
        pass  # look for session
    except Session.DoesNotExist:
        raise Http404("Session does not exist.")


def download_file(request, session, file):
    """Get single MP3 from session."""
    try:
        pass  # look for session
    except Session.DoesNotExist:
        raise Http404("Session does not exist.")

    try:
        pass  # look for file
    except AudioFile.DoesNotExist:
        raise Http404("File does not exist.")
