from django.contrib import admin
from solo.admin import SingletonModelAdmin

from archive.models import Challenge, Session, Artist, AudioFile


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("challenge", "number_of_tracks", "date")
    prepopulated_fields = {"slug": ("date",)}

    def number_of_tracks(self, obj):
        return obj.audiofile_set.count()


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_sessions", "copyright_ok")
    prepopulated_fields = {"slug": ("name",)}

    def number_of_sessions(self, obj):
        return obj.session_set.count()

    def copyright_ok(self, obj):
        return not obj.copyright_issues

    copyright_ok.boolean = True


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_tracks")
    prepopulated_fields = {"slug": ("name",)}

    def number_of_tracks(self, obj):
        return obj.audiofile_set.count()


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("filename", "artist", "duration", "challenge", "date")
    prepopulated_fields = {"slug": ("name",)}

    def duration(self, obj):
        return "{:02d}:{:02d}".format(obj.duration // 60, obj.duration % 60)

    def challenge(self, obj):
        return obj.session.challenge

    def date(self, obj):
        return obj.session.date
