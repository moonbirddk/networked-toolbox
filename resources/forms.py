
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .models import ToolResource


class ToolResourceEditForm(forms.ModelForm):
    class Meta:
        model = ToolResource
        fields = ['title']


class ToolResourceForm(forms.ModelForm):
    CONTENT_TYPES = [
        'pdf', 'docx', 'mp4', 'doc', 'ppt', 'pptx', 'mpeg4', 'avi',
        'mp3', 'png', 'jpeg', ''
    ]
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024

    class Meta:
        model = ToolResource
        fields = ['title', 'document']

    def clean_document(self):
        document = self.cleaned_data['document']
        content_type = document.content_type.split('/')[1]
        if content_type in self.CONTENT_TYPES:
            if document._size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    _('Please keep filesize under %s. Current filesize %s') %
                    (filesizeformat(self.MAX_UPLOAD_SIZE),
                     filesizeformat(document._size)))
        else:
            raise forms.ValidationError(_('File type is not allowed'))
        return document
