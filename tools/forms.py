import logging
from django import forms
from tools.models import ToolResource
from django_summernote.widgets import SummernoteInplaceWidget

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class ToolForm(forms.Form):
    title = forms.fields.CharField(max_length=100, required=True)
    cover_image = forms.fields.ImageField(required=False)
    description = forms.fields.CharField(
        widget=SummernoteInplaceWidget(), required=True)


class ToolCategoryForm(ToolForm):
    pass


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
