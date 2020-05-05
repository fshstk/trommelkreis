from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_sessions, name="all_sessions"),
    path("<session>.zip", views.download_session, name="zipdownload"),
    path("<session>/", views.show_session, name="sessionview"),
    path("<session>/<file>", views.download_file, name="fileview"),
]
