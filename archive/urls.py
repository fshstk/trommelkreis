from django.urls import path
from django.conf import settings

from archive import views

app_name = "archive"
urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.show_all_sessions, name="sessions"),
    path("artists/", views.show_all_artists, name="artists"),
    path("artists/<artist>", views.show_single_artist, name="single_artist"),
    # path("challenges/", views.show_all_challenges, name="challenges"),
    # path("challenges/<challenge>", views.show_single_challenge, name="single_challenge"),
    path("sessions/<session>.zip", views.download_session, name="single_session_zip"),
    path(
        "sessions/<session>/",
        views.show_single_session_if_no_copyright,
        name="single_session",
    ),
    path(
        "sessions/<session>/" + settings.MEDIA_PASSWORD,
        views.show_single_session,
        name="single_session_unconditional",
    ),
]
