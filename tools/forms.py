from django import forms
from django.conf import settings
from tools.models import Tool
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ToolForm(forms.Form):
    title = forms.fields.CharField(max_length=30, required=True)
    description = forms.fields.CharField(widget=SummernoteInplaceWidget(), required=True)
    cover_image = forms.fields.ImageField(required=False)

class ToolModelForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['title','description', 'cover_image' ]
        widgets = {'description': SummernoteInplaceWidget()}


