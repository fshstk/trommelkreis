from django.shortcuts import render
from django.http import Http404, JsonResponse

from archive.views import upload_form


def home(request):
    return render(request, "home.html")


def info(request):
    return render(request, "info.html")


def upload(request):
    # TODO: make this a global variable
    UPLOADS_OPEN = True

    if UPLOADS_OPEN:
        return upload_form(request)
    else:
        # TODO: downloads not open page
        raise Http404


def subscribe(request):
    return render(request, "subscribe.html")
