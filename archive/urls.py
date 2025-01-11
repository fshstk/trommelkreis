from django.urls import path
from django.conf import settings

from archive import views
from archive import api

app_name = "archive"
urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<session>/", views.single_session_if_no_copyright, name="single_session"),
    path("sessions/<session>/" + settings.MEDIA_PASSWORD, views.single_session_unconditional),
    path("api/sessions/<session>/", api.sessions_single),
]
