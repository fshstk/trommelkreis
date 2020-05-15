from django.contrib import admin
from solo.admin import SingletonModelAdmin

from archive.models import Challenge, Session, Artist, AudioFile, UploadFormVars

admin.site.register(Challenge)
admin.site.register(Session)
admin.site.register(Artist)
admin.site.register(AudioFile)
admin.site.register(UploadFormVars, SingletonModelAdmin)
