from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_all_sessions, name="archive_home"),
    path("<session>.zip", views.download_session, name="session_zip"),
    path("<session>/", views.show_single_session, name="session_view"),
]
