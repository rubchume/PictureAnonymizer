from django import forms

from core.models import Picture


class UploadPictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('picture', )
