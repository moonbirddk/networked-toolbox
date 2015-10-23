from django import forms
from django.conf import settings

class ToolForm(forms.Form):
    title = forms.fields.CharField(max_length=30, required=True)
    description = forms.fields.CharField(max_length=5000, widget=forms.Textarea, required=True)
    cover_image = forms.ImageField(required=False,upload_to= settings.MEDIA_ROOT + '/tools_images')