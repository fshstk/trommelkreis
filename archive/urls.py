from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<session>.zip", views.download_session, name="zipdownload"),
    path("<session>/", views.show_session, name="sessionview"),
    path("<session>/<file>", views.download_file, name="fileview"),
]
