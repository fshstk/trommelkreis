from django.urls import path
from django.conf import settings

from archive import views

app_name = "archive"
urlpatterns = [
    path("", views.show_all_sessions),  # TODO: use a redirect here
    path("sessions/", views.show_all_sessions, name="archive_home"),
    path("artists/", views.show_all_artists, name="artists"),
    path("artists/<artist>", views.show_single_artist, name="single_artist"),
    # path("challenges/", views.show_all_challenges, name="artists"),
    # path("challenges/<challenge>", views.show_single_challenge, name="single_challenge"),
    path("sessions/<session>.zip", views.download_session, name="session_zip"),
    path(
        "sessions/<session>/",
        views.show_single_session_if_no_copyright,
        name="session_view",
    ),
    path(
        "sessions/<session>/" + settings.MEDIA_PASSWORD,
        views.show_single_session,
        name="session_view_unconditional",
    ),
]
