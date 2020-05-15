from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from archive.views import upload_form
from archive.models import UploadFormVars


def home(request):
    return render(request, "home.html")


def info(request):
    return render(request, "info.html")


def upload(request):
    config = UploadFormVars.get_solo()

    if config.uploads_open:
        return upload_form(request)
    else:
        return render(request, "nexttime.html")


@csrf_exempt
def check_password(request):
    config = UploadFormVars.get_solo()

    if request.method == "POST":
        password = request.POST.get("password")
        return JsonResponse(
            {"valid": True if password == config.upload_password else False}
        )
    else:
        raise Http404


def subscribe(request):
    return render(request, "subscribe.html")
