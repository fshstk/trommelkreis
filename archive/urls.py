from django.urls import path
from django.conf import settings

from archive import views

urlpatterns = [
    path("", views.show_all_sessions, name="archive_home"),
    path("artists/", views.show_all_artists, name="artists"),
    path("artists/<artist>", views.show_single_artist, name="single_artist"),
    path("<session>.zip", views.download_session, name="session_zip"),
    path("<session>/", views.show_single_session_if_no_copyright, name="session_view"),
    path(
        "<session>/" + settings.MEDIA_PASSWORD,
        views.show_single_session,
        name="session_view_unconditional",
    ),
]
