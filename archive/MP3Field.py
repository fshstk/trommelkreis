"""
These classes were directly adapted from Django's built-in ImageField classes.
"""

from django import forms
from django.core import checks
from django.core.files.base import File
from django.db.models.fields.files import FileDescriptor, FieldFile, FileField
from django.db.models import signals


class MP3File(File):
    @property
    def duration(self):
        if not hasattr(self, "_duration_cache"):
            close = self.closed
            self.open()
            self._duration_cache = self._calculate_duration()
        return self._duration_cache

    def _calculate_duration(self):
        from mutagen.mp3 import EasyMP3

        mp3 = EasyMP3(self)
        return round(mp3.info.length)


class MP3FileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for MP3Fields. The only difference is
    assigning the duration to the duration_field, if appropriate.
    """

    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super().__set__(instance, value)

        # Only update duration if the field had a value before this assignment.
        # Since the default value for FileField subclasses is an instance of
        # field.attr_class, previous_file will only be None when we are called
        # from Model.__init__().  The MP3Field.update_duration_field method
        # hooked up to the post_init signal handles the Model.__init__() cases.
        # Assignment happening outside of Model.__init__() will trigger the
        # update right here.
        if previous_file is not None:
            self.field.update_duration_field(instance, force=True)


class MP3FieldFile(MP3File, FieldFile):
    def delete(self, save=True):
        # Clear the mp3 duration cache
        if hasattr(self, "_duration_cache"):
            del self._duration_cache
        super().delete(save)


class MP3FormField(forms.fields.FileField):
    # TODO: See forms.fields.ImageField for inspiration.
    # Right now this does nothing, but we should add checks for file suffix,
    # using mutagen to check MP3 validity, etc.
    pass


class MP3Field(FileField):
    attr_class = MP3FieldFile
    descriptor_class = MP3FileDescriptor
    description = "MP3 File"

    def __init__(self, verbose_name=None, name=None, duration_field=None, **kwargs):
        self.duration_field = duration_field
        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_mp3_library_installed(),
        ]

    def _check_mp3_library_installed(self):
        try:
            from mutagen.mp3 import EasyMP3
        except ImportError:
            return [
                checks.Error(
                    "Cannot use MP3Field because mutagen is not installed.",
                    hint=(
                        "Get mutagen at https://pypi.org/project/mutagen/ "
                        'or run command "python -m pip install mutagen".'
                    ),
                    obj=self,
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.duration_field:
            kwargs["duration_field"] = self.duration_field
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        # Attach update_duration_field so that duration fields declared
        # after their corresponding mp3 field don't stay cleared by
        # Model.__init__.
        # Only run post-initialization duration update on non-abstract models
        if not cls._meta.abstract:
            signals.post_init.connect(self.update_duration_field, sender=cls)

    def update_duration_field(self, instance, force=False, *args, **kwargs):
        """
        Update field's duration field, if defined.

        This method is hooked up to model's post_init signal to update
        duration after instantiating a model instance.  However, duration
        won't be updated if the duration field is already populated.  This
        avoids unnecessary recalculation when loading an object from the
        database.

        Duration can be forced to update with force=True, which is how
        MP3FileDescriptor.__set__ calls this method.
        """
        # Nothing to update if the field doesn't have a duration field or if
        # the field is deferred.
        if not self.duration_field or self.attname not in instance.__dict__:
            return

        # getattr will call the MP3FileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (MP3FieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        duration_field_filled = not (
            self.duration_field and not getattr(instance, self.duration_field)
        )

        # When duration field has a value, we are most likely loading
        # data from the database or updating an mp3 field that already had
        # an mp3 stored.  In the first case, we don't want to update the
        # duration field because we are already getting its value from the
        # database.  In the second case, we do want to update the durration
        # field and will skip this return because force will be True since we
        # were called from MP3FileDescriptor.__set__.
        if duration_field_filled and not force:
            return

        # file should be an instance of MP3FieldFile or should be None.
        if file:
            duration = file.duration
        else:
            # No file, so clear duration field.
            duration = None

        # Update the duration field.
        if self.duration_field:
            setattr(instance, self.duration_field, duration)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": MP3FormField,
                **kwargs,
            }
        )
