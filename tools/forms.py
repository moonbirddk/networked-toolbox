import logging

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django_summernote.widgets import SummernoteInplaceWidget
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import LazyTypedChoiceField
from django_countries import countries
from django.contrib.contenttypes.models import ContentType

from .models import Tool, ToolCategory, CategoryGroup, Story
from .widgets import ColumnCheckboxSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple
log = logging.getLogger(__name__)

from trumbowyg.widgets import TrumbowygWidget


def get_trumbowyg_form_for_model(model_name, text_field, fields='__all__', excludes=None):
    content_type = ContentType.objects.get(model=model_name)
    model_class = content_type.model_class()
    form_fields = fields

    class _ObjectForm(forms.ModelForm):
        class Meta:
            model = model_class
            exclude = (excludes,)
            widgets = {
                text_field: TrumbowygWidget(),
            }


    return _ObjectForm


class OverviewPageForm(forms.Form):
    description = forms.fields.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea
    )


class ToolCategoryChoiceField(forms.ModelMultipleChoiceField):

    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, queryset=None, **kwargs):
        if not queryset:
            queryset = ToolCategory.objects.all()
        super().__init__(queryset=queryset, **kwargs)

    def label_from_instance(self, obj):
        return obj.title


class CategoryGroupForm(forms.Form):
    name = forms.fields.CharField(max_length=30, required=True)
    description = forms.fields.CharField(widget=forms.Textarea,
                           max_length=255,
                           required=False,
                           help_text='255 characters max.')
    categories = ToolCategoryChoiceField(label='Toolboxes')


class ToolForm(forms.Form):
    published = forms.fields.BooleanField(
        required=False,
        label="Published (available for all users)"
    )
    title = forms.fields.CharField(max_length=100, required=True)
    resources_text = forms.fields.CharField(
        max_length=300
    )
    cover_image = forms.fields.ImageField(
        required=False,
        label='Cover image (recommended size: 1200x600)'
    )
    description = forms.fields.CharField(
        widget=SummernoteInplaceWidget(),
        required=True,
        max_length=20000
    )
    categories = ToolCategoryChoiceField(label='Toolboxes')


class StoryForm(forms.ModelForm):
    #title = forms.fields.CharField(max_length=100, required=True)
    class Meta: 
        model = Story 
        fields = ('title', 'content', 'country', 'associated_tools',)
        widgets = {
            'content': SummernoteInplaceWidget(), 
            'associated_tools': CheckboxSelectMultiple,
            #     columns=3,
            #     css_class='col-md-4', 
            #     wrapper_css_class='row',
                
            #    ),
        }
  
   


class ToolCategoryForm(forms.Form):
    published = forms.fields.BooleanField(
        required=False,
        label="Published (available for all users)"
    )
    title = forms.fields.CharField(max_length=100, required=True)
    resources_text = forms.fields.CharField(
        max_length=300
    )
    cover_image = forms.fields.ImageField(
        required=False,
        label='Cover image (recommended size: 1200x600)'
    )
    description = forms.fields.CharField(
        widget=SummernoteInplaceWidget(),
        required=True,
        max_length=20000
    )
    group = forms.ModelChoiceField(label='Work Area',
                                   queryset=CategoryGroup.objects.all(),
                                   required=True)


class SuggestionRelatedObjectForm(forms.Form):
    _rel_obj_type_choices = (
        ('tool', 'tool'),
        ('category', 'category'),
        ('categorygroup', 'categorygroup'),
    )

    RELATED_OBJECT_MODELS = {
        'tool': Tool, 
        'category': ToolCategory, 
        'categorygroup': CategoryGroup, 
    }
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
            obj = self.RELATED_OBJECT_MODELS[rel_obj_type].objects.get(id=rel_obj_id)
        
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
