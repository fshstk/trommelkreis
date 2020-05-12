from django.contrib import admin

from archive.models import Challenge, Session, Artist, AudioFile

admin.site.register(Challenge)
admin.site.register(Session)
admin.site.register(Artist)
admin.site.register(AudioFile)
