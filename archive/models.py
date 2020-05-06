from django.db import models
from django.utils import timezone

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
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, unique=True)
    info = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.slug

    @classmethod
    def grouped_by_month(cls):
        sessions = cls.objects.order_by("date")
        grouped_sessions = []
        for _, group in groupby(sessions, key=lambda x: x.date.strftime("%B%Y")):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @property
    def slug(self):
        return self.date.strftime("%Y%m%d")

    # TODO: move this to the view layer
    @property
    def datestring(self):
        return self.date.strftime("%d.%m.%Y")

    @property
    def files(self):
        return self.audiofile_set.all()

    # TODO: move this to the view layer
    @property
    def filecount_string(self):
        filecount = len(self.files)
        if filecount is 0:
            return "Keine Einträge"
        elif filecount is 1:
            return "1 Eintrag"
        else:
            return "{} Einträge".format(filecount)


# TODO: do we REALLY need this class? can we not solve everything w/ just queries...
class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    @property
    def files(self):
        return self.audiofile_set.all()


class AudioFile(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    data = models.FileField(upload_to="archive/%Y%m%d/")
    # just read ID3 tag for artist/name?
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)

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
    def mp3(self):
        filepath = os.path.join(settings.MEDIA_ROOT, self.data.name)
        return EasyMP3(filepath)

    @property
    def duration(self):
        return round(self.mp3.info.length)
