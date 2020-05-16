from django.contrib import admin
from solo.admin import SingletonModelAdmin

from archive.models import Challenge, Session, Artist, AudioFile, UploadFormVars

admin.site.register(UploadFormVars, SingletonModelAdmin)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("displayname",)
    prepopulated_fields = {"slug": ("date",)}

    def displayname(self, obj):
        return "{}: {} {}".format(
            obj.slug, obj.challenge.name, "©" if obj.challenge.copyright_issues else "",
        )

    displayname.short_description = "Name"


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("displayname",)
    prepopulated_fields = {"slug": ("name",)}

    def displayname(self, obj):
        return "{} ({} Session/s)".format(obj.name, obj.session_set.count(),)

    displayname.short_description = "Name"


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("displayname",)
    prepopulated_fields = {"slug": ("name",)}

    def displayname(self, obj):
        return "{} ({} Tracks)".format(
            obj.name if obj.name else "<Anon>", obj.audiofile_set.count(),
        )

    displayname.short_description = "Name"


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("displayname",)
    prepopulated_fields = {"slug": ("name",)}

    def displayname(self, obj):
        return "{} [{}] ({})".format(
            obj.filename,
            obj.artist.name if obj.artist.name else "<Anon>",
            "{:02d}:{:02d}".format(obj.duration // 60, obj.duration % 60),
        )

    displayname.short_description = "Name"
