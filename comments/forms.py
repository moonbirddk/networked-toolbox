import logging

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from tools.models import Tool, ToolCategory
from .models import Comment


log = logging.getLogger(__name__)


def no_url_in_content_validator(value):
    if 'http' in value:
        raise ValidationError("Comment can not contain URL")


class CommentForm(forms.Form):
    _rel_obj_type_choices = (
        ('tool', 'tool'),
        ('toolcategory', 'toolcategory'),
        ('comment', 'comment'),
    )

    content = forms.CharField(
        validators=[no_url_in_content_validator, ],
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

    def clean(self):
        super().clean()
        rel_obj_id = self.cleaned_data.get('related_object_id')
        rel_obj_type = self.cleaned_data.get('related_object_type')
        if rel_obj_id and rel_obj_type:
            try:
                if rel_obj_type == 'tool':
                    obj = Tool.objects.get(id=rel_obj_id)
                elif rel_obj_type == 'toolcategory':
                    obj = ToolCategory.objects.get(id=rel_obj_id)
                elif rel_obj_type == 'comment':
                    obj = Comment.objects.get(id=rel_obj_id)
                    if obj.related_object_type == 'comment':
                        raise ValidationError("Commenting on a comment"
                                              "of a comment is not allowed.")
                else:
                    raise ValidationError("Not allowed related object type")
            except ObjectDoesNotExist as exc:
                raise ValidationError("Non existent related object")
            self.cleaned_data['related_object'] = obj
        return self.cleaned_data

