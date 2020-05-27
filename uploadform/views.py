from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

from uploadform.models import UploadFormVars
from uploadform.forms import UploadForm


def upload(request):
    config = UploadFormVars.get_solo()

    if config.uploads_open:
        return upload_form(request)
    else:
        return render(request, "uploadform/nexttime.html")


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


def upload_form(request):
    config = UploadFormVars.get_solo()
    today = config.session

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            uploaded_file.session = today
            uploaded_file.save()
            return HttpResponseRedirect(
                reverse("archive:single_session", args=[today.slug])
            )
    else:
        form = UploadForm()

    return render(
        request,
        "uploadform/upload.html",
        {"form": form, "today": today, "info": config.session_info},
    )
