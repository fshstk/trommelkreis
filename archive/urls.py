from django.urls import path
from django.conf import settings

from archive import views
from archive import api

app_name = "archive"
urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<slug>/", views.single_session, name="single_session"),
    path("api/sessions/<slug>/", api.sessions_single),
]
