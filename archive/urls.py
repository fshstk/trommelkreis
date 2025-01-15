from django.urls import path
from django.conf import settings

from archive import views
from archive import api

app_name = "archive"
urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<slug>/", views.single_session_if_no_copyright, name="single_session"),
    path(f"sessions/<slug>/{settings.MEDIA_PASSWORD}", views.single_session_unconditional),
    path("api/sessions/<slug>/", api.sessions_single),
]
