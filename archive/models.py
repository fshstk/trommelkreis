from django.db import models
from django.utils import timezone
from django.db.models.functions import TruncMonth
from solo.models import SingletonModel
from django.utils.text import slugify

from datetime import datetime
from itertools import groupby
from mutagen.mp3 import EasyMP3
import os.path


class SlugIncluded(models.Model):
    """
    Abstract base class for database models that auto-generates unique slug on save.
    Must override slug_basename() in child class with chosen base name.
    """

    class Meta:
        abstract = True

    slug = models.SlugField(unique=True, null=False, max_length=50)

    def slug_basename(self):
        """Define what base name is used to auto-generate slug."""
        raise NotImplementedError

    @classmethod
    def generate_unique_slug(cls, basename):
        max_basename_length = 40
        slug_basename = slugify(basename)[:max_basename_length]
        slug = slug_basename
        num = 1
        while cls.objects.filter(slug=slug).exists():
            num += 1
            slug = "{}-{}".format(slug_basename, num)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(basename=self.slug_basename())
        super().save(*args, **kwargs)


class Challenge(SlugIncluded):
    name = models.CharField(max_length=200, unique=True)
    blurb = models.TextField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    copyright_issues = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def sessions(self):
        return self.session_set.all()

    def slug_basename(self):
        return self.name


class Session(SlugIncluded):
    challenge = models.ForeignKey(Challenge, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    info = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.slug

    def slug_basename(self):
        return self.date.strftime("%Y%m%d")

    @classmethod
    def grouped_by_month(cls):
        sessions = cls.objects.order_by("date").annotate(month=TruncMonth("date"))
        grouped_sessions = []
        for _, group in groupby(sessions, key=lambda x: x.month):
            grouped_sessions.append(list(group))
        return grouped_sessions

    @classmethod
    def from_slug(cls, slug):
        # TODO: get rid of this
        return cls.objects.get(slug=slug)

    @property
    def files(self):
        return self.audiofile_set.all()

    @property
    def copyright_issues(self):
        return self.challenge.copyright_issues


class Artist(SlugIncluded):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def slug_basename(self):
        return self.name

    @property
    def files(self):
        return self.audiofile_set.all()


class AudioFile(SlugIncluded):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    data = models.FileField(upload_to="archive/")
    artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)

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
        return self.data.path

    @property
    def mp3(self):
        return EasyMP3(self.filepath)

    @property
    def duration(self):
        return round(self.mp3.info.length)

    @property
    def url(self):
        # TODO: this returns an extra "/media" at the start of the url
        return self.data.url

    def slug_basename(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        mp3 = self.mp3
        if self.name:
            mp3["title"] = self.name
        if self.artist.name:
            mp3["artist"] = self.artist.name
        mp3.save()


class UploadFormVars(SingletonModel):
    class Meta:
        verbose_name_plural = "Upload form variables"

    session = models.ForeignKey(
        Session, blank=True, null=True, on_delete=models.SET_NULL
    )
    uploads_open = models.BooleanField(default=False)
    upload_password = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return "Upload Form Variables"
