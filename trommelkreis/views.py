from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def info(request):
    return render(request, "info.html")


def upload(request):
    return render(request, "upload.html")


def subscribe(request):
    return render(request, "subscribe.html")
