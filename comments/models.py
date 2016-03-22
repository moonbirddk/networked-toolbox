import datetime, time

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


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

    def to_data(self):
        return {
            'id': self.id,
            'added_dt': self.added_dt.isoformat(),
            'timestamp': int(time.mktime(self.added_dt.timetuple())) * 1000,
            'related_object_id': self.related_object_id,
            'related_object_type': self.related_object_type.model,
            'author_username': self.author.username,
            'author_first_name': self.author.first_name,
            'author_last_name': self.author.last_name,
            'content': self.content,
        }
