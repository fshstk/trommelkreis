from django.forms import Form, ModelForm, ValidationError
from django.forms import CharField, BooleanField, FileField

from mutagen.mp3 import EasyMP3

from archive.models import AudioFile, Artist


def validate_password(password):
    # TODO: we can get away with not using any custom Field classes or validator functions
    # if we do the password checking via ajax before the form is presented
    correct_password = "20200406"  # TODO: query this dynamically
    if password != correct_password:
        raise ValidationError("Wrong password!")


# def validate_mp3(file):
#     print (type(file))


class MP3Field(FileField):
    pass
    # def clean(self, value):
    #     print("hi")
    #     return super().clean(value)


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
            print("DOOOES NOT EXIIIIST")
            return Artist(name=artistname)


class UploadForm(ModelForm):
    artist = ArtistField(required=False)
    data = MP3Field()
    password = CharField(max_length=20, validators=[validate_password])
    tos = BooleanField(required=True)

    class Meta:
        model = AudioFile
        fields = ["name", "data"]

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
