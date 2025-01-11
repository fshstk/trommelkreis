from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_safe
from archive.models import Session


@require_safe
def sessions_single(request, session):
    try:
        session = Session.objects.get(slug=session)
    except Session.DoesNotExist:
        return HttpResponse(f"Session '{session}' not found", status=404)

    return JsonResponse({
        "date": session.date.strftime("%Y-%m-%d"),
        "url": request.build_absolute_uri(reverse("archive:single_session", args=[session.slug])),
        "challenge": {
            "name": session.challenge.name,
            "blurb": session.challenge.blurb,
        },
        "tracks": [{
            "name": track.name,
            "artist": track.artist.name if track.artist else "",
            "duration": "{:02d}:{:02d}".format(track.duration // 60, track.duration % 60),
            "sessionSubsection": track.session_subsection,
            "url": track.url,
        } for track in session.files],
    })
