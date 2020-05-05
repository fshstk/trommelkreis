from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Challenge, Session, Artist, AudioFile


def index(request):
    """Show archive index."""
    pass


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
