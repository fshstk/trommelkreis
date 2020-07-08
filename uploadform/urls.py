from django.urls import path
from django.conf import settings

from uploadform import views

app_name = "upload"
urlpatterns = [
    path("", views.upload, name="index"),
    path(settings.PREVIEW_PASSWORD, views.preview),
    path("checkpassword/", views.check_password),
]
