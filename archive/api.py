from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from archive.models import Session


def sessions_single(request, session):
    try:
        session = Session.objects.get(slug=session)
    except Session.DoesNotExist:
        return JsonResponse({
            "data": {
                "session": None,
            }
        }, status=404)

    return JsonResponse({
        "data": {
            "session": {
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
            }
        }
    })
