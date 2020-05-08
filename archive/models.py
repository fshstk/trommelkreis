from django.db import models
from django.utils import timezone
from django.db.models.functions import TruncMonth

from itertools import groupby
from mutagen.mp3 import EasyMP3
import os.path

from trommelkreis import settings


class Challenge(models.Model):
    name = models.CharField(max_length=200, unique=True)
    blurb = models.TextField(max_length=1000, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def sessions(self):
        return self.session_set.all()


class Session(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now, unique=True)
    info = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.slug

    @classmethod
    def grouped_by_month(cls):
        sessions = cls.objects.order_by("date").annotate(month=TruncMonth("date"))
        grouped_sessions = []
        for _, group in groupby(sessions, key=lambda x: x.month):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @property
    def slug(self):
        return self.date.strftime("%Y%m%d")

    @property
    def files(self):
        return self.audiofile_set.all()


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    @property
    def files(self):
        return self.audiofile_set.all()


class AudioFile(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    data = models.FileField(upload_to="archive/%Y%m%d/")  # TODO: dynamic upload path?
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "name"], name="unique_name_per_session"
            )
        ]

    def __str__(self):
        return self.name

    @property
    def filesize(self):
        return self.data.size

    @property
    def filename(self):
        return os.path.basename(self.data.name)

    @property
    def filepath(self):
        """Returns full path to file on disk (do not expose)."""
        return os.path.join(settings.MEDIA_ROOT, self.data.name)

    @property
    def mp3(self):
        return EasyMP3(self.filepath)

    @property
    def duration(self):
        return round(self.mp3.info.length)

    @property
    def url(self):
        return self.data.url
