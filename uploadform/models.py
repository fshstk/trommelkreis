from django.db import models
from solo.models import SingletonModel


class UploadFormVars(SingletonModel):
    class Meta:
        verbose_name = "Upload form variables"
        verbose_name_plural = "Upload form variables"

    session = models.ForeignKey(
        "archive.Session", blank=True, null=True, on_delete=models.SET_NULL
    )
    uploads_open = models.BooleanField(default=False)
    upload_password = models.CharField(blank=True, max_length=20)
    session_info = models.TextField(blank=True, max_length=1000)

    def __str__(self):
        return "Upload Form Variables"
