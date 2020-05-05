from django.shortcuts import render, get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear

from math import ceil

from archive.models import Session


def show_all_sessions(request):
    archive = [split_list_in_half(month) for month in Session.grouped_by_month()]
    archive.reverse()  # Reverse chronoloical order
    context = {"archive": archive}  # "archive": sessions.group_by_month
    return render(request, "archive/index.html", context)


def download_session(request, session):
    """Get all session files as zip archive."""
    try:
        pass  # look for session
    except Session.DoesNotExist:
        raise Http404("Session does not exist.")


def show_single_session(request, session):
    try:
        pass  # look for session
    except Session.DoesNotExist:
        raise Http404("Session does not exist.")


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


def filesize_to_string(numbytes):
    kB = 1000
    MB = kB ** 2
    if nunmbytes > MB:
        return "{:.2f} MB".format(numbytes / MB)
    else:
        return "{:.0f} kB".format(numbytes / kB)


def duration_to_string(numseconds):
    return "{:02d}:{:02d}".format(numseconds // 60, numseconds % 60)
