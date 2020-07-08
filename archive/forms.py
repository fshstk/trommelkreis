from django import forms
from pagedown.widgets import AdminPagedownWidget

from archive.models import Challenge


class ChallengeForm(forms.ModelForm):
    description = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Challenge
        fields = "__all__"

