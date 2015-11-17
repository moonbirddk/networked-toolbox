import logging

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django_summernote.widgets import SummernoteInplaceWidget
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .models import Tool, ToolResource, ToolCategory, Suggestion


log = logging.getLogger(__name__)


class ToolCategoryChoiceField(forms.ModelMultipleChoiceField):

    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        queryset = ToolCategory.objects.all()
        super().__init__(queryset=queryset, **kwargs)

    def label_from_instance(self, obj):
        return obj.title


class ToolForm(forms.Form):
    title = forms.fields.CharField(max_length=100, required=True)
    cover_image = forms.fields.ImageField(
        required=False,
        label='Cover image (recommended size: 1200x600)'
    )
    description = forms.fields.CharField(
        widget=SummernoteInplaceWidget(), required=True)
    categories = ToolCategoryChoiceField()


class ToolCategoryForm(forms.Form):
    title = forms.fields.CharField(max_length=100, required=True)
    cover_image = forms.fields.ImageField(
        required=False,
        label='Cover image (recommended size: 1200x600)'
    )
    description = forms.fields.CharField(
        widget=SummernoteInplaceWidget(), required=True)


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


class SuggestionRelatedObjectForm(forms.Form):
    _rel_obj_type_choices = (
        ('tool', 'tool'),
        ('category', 'category'),
    )

    related_object_type = forms.fields.ChoiceField(
        choices=_rel_obj_type_choices,
        required=True,
        widget=forms.fields.HiddenInput()
    )
    related_object = forms.fields.IntegerField(
        required=True,
        widget=forms.fields.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        rel_obj_id = cleaned_data['related_object']
        rel_obj_type = self.cleaned_data['related_object_type']
        try:
            if rel_obj_type == 'tool':
                obj = Tool.objects.get(id=rel_obj_id)
            elif rel_obj_type == 'category':
                obj = ToolCategory.objects.get(id=rel_obj_id)
        except ObjectDoesNotExist as exc:
            raise ValidationError("Non existent related object")

        self.cleaned_data['related_object'] = obj
        return self.cleaned_data


class SuggestionForm(forms.Form):
    description = forms.fields.CharField(required=True,
                                         widget=forms.Textarea)
    attachement = forms.fields.FileField(required=False)

    CONTENT_TYPES = [
        'pdf', 'docx', 'mp4', 'doc', 'ppt', 'pptx', 'mpeg4', 'avi',
        'mp3', 'png', 'jpeg', ''
    ]
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024

    def clean_attachement(self):
        if 'attachement' not in self.cleaned_data or\
                not self.cleaned_data['attachement']:
            return
        attachement = self.cleaned_data['attachement']
        content_type = attachement.content_type.split('/')[1]
        if content_type in self.CONTENT_TYPES:
            if attachement._size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    _('Please keep filesize under %s. Current filesize %s') %
                    (filesizeformat(self.MAX_UPLOAD_SIZE),
                     filesizeformat(attachement._size)))
        else:
            raise forms.ValidationError(_('File type is not allowed'))
        return attachement
