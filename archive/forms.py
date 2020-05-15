from django.forms import Form, ModelForm, ValidationError
from django.forms import CharField, BooleanField, FileField

from mutagen.mp3 import EasyMP3, HeaderNotFoundError

from archive.models import AudioFile, Artist, UploadFormVars


def validate_password(password):
    # TODO: we can get away with not using any custom Field classes or validator functions
    # if we do the password checking via ajax before the form is presented
    config = UploadFormVars.get_solo()
    if password != config.upload_password:
        raise ValidationError("Wrong password!")


class MP3Field(FileField):
    def clean(self, value, initial=None):
        file = super().clean(value, initial)

        if not file.name.endswith(".mp3"):
            raise ValidationError("file name does not end in .mp3")
        try:
            mp3 = EasyMP3(file.temporary_file_path())
        except HeaderNotFoundError:
            raise ValidationError("file is not a valid mp3")
        if mp3.info.sketchy:
            raise ValidationError("file may not be a valid mp3")
        return file


class ArtistField(CharField):
    def __init__(self, max_length=None, **kwargs):
        if max_length is None:
            max_length = Artist._meta.get_field("name").max_length
        super().__init__(max_length=max_length, **kwargs)

    def clean(self, value):
        artistname = super().clean(value)
        try:
            return Artist.objects.get(name=artistname)
        except Artist.DoesNotExist:
            # Return a new Artist object, but don't save it to the database
            # until the rest of the form has been validated:
            return Artist(name=artistname)


class UploadForm(ModelForm):
    artist = ArtistField(required=False)
    data = MP3Field()
    password = CharField(max_length=20, validators=[validate_password])
    tos = BooleanField(required=True)

    class Meta:
        model = AudioFile
        fields = ["name", "data", "artist"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["artist"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Dein Name"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Passwort"}
        )
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Name deines Tracks"}
        )
        self.fields["data"].widget.attrs.update({"class": "custom-file-input"})
        self.fields["tos"].widget.attrs.update({"class": "form-check-input"})

    def save(self, commit=True):
        config = UploadFormVars.get_solo()

        instance = super().save(commit=False)
        instance.session = config.session
        if commit:
            if instance.artist is not None:
                instance.artist.save()
            instance.save()
        return instance
