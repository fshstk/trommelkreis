from django.contrib import admin
from solo.admin import SingletonModelAdmin

from archive.models import Challenge, Session, Artist, AudioFile
from archive.forms import ChallengeForm


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_display = ("challenge", "number_of_tracks", "date")
    # list_filter = ("challenge",)
    search_fields = ["challenge__name"]
    prepopulated_fields = {"slug": ("date",)}

    def number_of_tracks(self, obj):
        return obj.tracks.count()

    # number_of_tracks.admin_order_field = Count("audiofile")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_sessions", "copyright_ok")
    # list_filter = ("copyright_ok",)
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    form = ChallengeForm

    def number_of_sessions(self, obj):
        return obj.session_set.count()

    def copyright_ok(self, obj):
        return not obj.copyright_issues

    copyright_ok.boolean = True


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "number_of_tracks")
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    def number_of_tracks(self, obj):
        return obj.tracks.count()


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    date_hierarchy = "session__date"
    list_display = ("date", "challenge", "filename", "artist", "duration")
    list_display_links = ("filename",)
    # list_filter = ("artist",)
    search_fields = ["name", "session__challenge__name", "artist__name"]
    prepopulated_fields = {"slug": ("name",)}

    def duration(self, obj):
        return "{:02d}:{:02d}".format(obj.duration // 60, obj.duration % 60)

    def challenge(self, obj):
        return obj.session.challenge

    challenge.admin_order_field = "session__challenge__name"

    def date(self, obj):
        return obj.session.date

    date.admin_order_field = "session__date"
