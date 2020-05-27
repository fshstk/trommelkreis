from django.urls import path
from django.conf import settings

from archive import views

app_name = "archive"
urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.sessions, name="sessions"),
    path("artists/", views.artists, name="artists"),
    path("artists/<artist>", views.single_artist, name="single_artist"),
    # path("challenges/", views.challenges, name="challenges"),
    # path("challenges/<challenge>", views.single_challenge, name="single_challenge"),
    path("sessions/<session>.zip", views.download_session, name="download_session"),
    path("sessions/<session>/", views.single_session_if_no_copyright, name="single_session"),
    path("sessions/<session>/" + settings.MEDIA_PASSWORD, views.single_session_unconditional),
]
