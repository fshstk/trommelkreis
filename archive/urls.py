from django.urls import path

from archive import views

urlpatterns = [
    path("", views.show_all_sessions, name="archive_home"),
    path("<session>.zip", views.download_session, name="session_zip"),
    path("<session>/", views.show_single_session_if_no_copyright, name="session_view"),
    path(
        "<session>/fuckgema",
        views.show_single_session,
        name="session_view_unconditional",
    ),
]
