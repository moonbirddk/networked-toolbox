from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .utils import format_added_dt


class Comment(models.Model):
    related_object_type = models.ForeignKey(
        ContentType,
        null=False,
        blank=False
    )
    related_object_id = models.PositiveIntegerField(null=False, blank=False)
    related_object = GenericForeignKey('related_object_type',
                                       'related_object_id')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False
    )
    content = models.TextField(max_length=settings.COMMENT_MAX_LENGTH)
    added_dt = models.DateTimeField(auto_now_add=True)
