from django.db import models
from django.utils import timezone

from itertools import groupby


class Challenge(models.Model):
    name = models.CharField(max_length=200, unique=True)
    blurb = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, unique=True)

    def __str__(self):
        return self.slug

    @classmethod
    def grouped_by_month(cls):
        sessions = cls.objects.order_by("date")
        grouped_sessions = []
        for _, group in groupby(sessions, key=lambda x: x.monthyear):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @property
    def slug(self):
        return self.date.strftime("%Y%m%d")

    @property
    def month(self):
        return self.date.strftime("%B")

    @property
    def year(self):
        return self.date.strftime("%Y")

    @property
    def monthyear(self):
        return self.date.strftime("%B %Y")

    @property
    def datestring(self):
        return self.date.strftime("%d.%m.%Y")

    @property
    def filecount_string(self):
        filecount = len(self.files)
        if filecount is 0:
            return "Keine Einträge"
        elif filecount is 1:
            return "1 Eintrag"
        else:
            return "{} Einträge".format(filecount)


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
