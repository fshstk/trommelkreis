from django.db import models
from django.utils import timezone


class Challenge(models.Model):
    name = models.CharField(max_length=200, unique=True)
    blurb = models.CharField(max_length=1000, blank=True)
    longtext = models.CharField(max_length=5000, blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.date


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class AudioFile(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    data = models.FileField(upload_to="archive/%Y%m%d/")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "name"], name="unique_name_per_session"
            )
        ]

    def __str__(self):
        return self.name
