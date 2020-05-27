from django.shortcuts import render, redirect


def index(request):
    return redirect("home")


def home(request):
    return render(request, "home.html")


def info(request):
    return render(request, "info.html")


def subscribe(request):
    return render(request, "subscribe.html")
