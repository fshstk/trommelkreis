from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        return render(request, "nexttime.html")


@csrf_exempt
def check_password(request):
    # TODO: make this a global variable
    CORRECT_PASSWORD = "foobar"

    if request.method == "POST":
        password = request.POST.get("password")
        return JsonResponse({"valid": True if password == CORRECT_PASSWORD else False})
    else:
        raise Http404


def subscribe(request):
    return render(request, "subscribe.html")
