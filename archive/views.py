from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse
from django.views.decorators.http import require_safe
from django.views.decorators.cache import never_cache
from django.db.models import Count, F

from math import ceil
from datetime import datetime
import io
from itertools import groupby

from archive.models import Challenge, Artist, Session


def index(request):
    return redirect("archive:sessions")


def sessions(request):
    sessions = Session.objects.order_by("date").annotate(
        month=TruncMonth("date"),
        num_tracks=Count("tracks"),
        challenge_name=F("challenge__name"),
        blurb=F("challenge__blurb"),
        restricted=F("challenge__copyright_issues"),
    ).filter(num_tracks__gt=0)
    archive = [list(group) for _, group in groupby(sessions, key=lambda x: x.month)]
    archive = [
        [month[:ceil(len(month) / 2)],
        month[ceil(len(month) / 2):]
    ] for month in archive]
    archive.reverse()
    return render(request, "archive/sessions_all.html", {"archive": archive})


@require_safe
def single_session(request, slug):
    session = get_object_or_404(Session, slug=slug)
    return render(request, "archive/sessions_single.html", {
        "session": session,
        "files": [{
            "name": file.name,
            "slug": file.slug,
            "artist": file.artist.name if file.artist else "Anonym",
            "url": file.url,
            "subsection": file.session_subsection
        } for file in session.tracks.select_related("artist").all()],
    })
