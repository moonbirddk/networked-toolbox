import logging

import bleach
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from tools.models import Tool, ToolCategory, Story
from library.models import LibraryDocument, VideoResource, OnlineCourse
from .models import ThreadedComment


log = logging.getLogger(__name__)


def no_urls_validator(value):
    if 'http' in value and '://' in value:
        raise ValidationError("Comment can not contain URL")


class CommentForm(forms.Form):
    _rel_obj_type_cls = {
        'tool': Tool,
        'story': Story,
        'toolcategory': ToolCategory,
        'librarydocument': LibraryDocument, 
        'onlinecourse': OnlineCourse, 
        'videoresource': VideoResource
    }
    _rel_obj_type_choices = tuple(
        [(k, k) for k in _rel_obj_type_cls.keys()]
    )

    content = forms.CharField(
        validators=[no_urls_validator, ],
        widget=forms.Textarea,
        max_length=settings.COMMENT_MAX_LENGTH,
        required=True
    )

    related_object_type = forms.ChoiceField(
        choices=_rel_obj_type_choices,
        required=True,
        widget=forms.fields.HiddenInput()
    )
    related_object_id = forms.fields.IntegerField(
        required=True,
        widget=forms.fields.HiddenInput()
    )

    parent = forms.ModelChoiceField(
        queryset=ThreadedComment.objects.filter(parent__isnull=True),
        required=False, widget=forms.HiddenInput
    )

    def clean(self):
        super().clean()
        rel_obj_id = self.cleaned_data.get('related_object_id')
        rel_obj_type = self.cleaned_data.get('related_object_type')
        if rel_obj_id and rel_obj_type:
            try:
                rel_cls = self._rel_obj_type_cls[rel_obj_type]
                obj = rel_cls.objects.get(id=rel_obj_id)
            except KeyError:
                    raise ValidationError("Not allowed related object type")
            except ObjectDoesNotExist:
                raise ValidationError("Non existent related object")
            self.cleaned_data['related_object'] = obj
        return self.cleaned_data

    def clean_content(self):
        if 'content' in self.cleaned_data:
            newval = \
                bleach.clean(self.cleaned_data['content'], tags=[],
                             strip=True, strip_comments=True)
            self.cleaned_data['content'] = newval
            return newval
