from django.contrib import admin
from solo.admin import SingletonModelAdmin

from uploadform.models import UploadFormVars

admin.site.register(UploadFormVars, SingletonModelAdmin)
