
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from notifications.signals import notify

from tools.models import Tool


class ThreadedCommentManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().order_by('tree_id', 'added_dt')

    def get_parents(self):
        return self.get_queryset().filter(parent__isnull=True)


class ThreadedComment(models.Model):
    related_object_type = models.ForeignKey(
        ContentType,
        null=False,
        blank=False
    )
    related_object_id = models.PositiveIntegerField(null=False, blank=False)
    related_object = GenericForeignKey('related_object_type',
                                       'related_object_id')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        related_name='children'
    )
    tree_id = models.IntegerField(null=True, blank=False, db_index=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False
    )
    content = models.TextField(max_length=settings.COMMENT_MAX_LENGTH)
    added_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    is_removed = models.BooleanField(default=False)
    edited_dt = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['tree_id', 'added_dt']


def notify_author(sender, instance, created, **kwargs):
    if created:
        actions = []
        if instance.related_object_type.model == 'story':
            recipient = instance.related_object.user
            href = instance.related_object.get_absolute_url()
            href += '#comment-' + str(instance.id)
            actions.append({
                'title': 'read',
                'href': href
            })
            notify.send(instance.author,
                        verb='commented on your story',
                        recipient=instance.related_object.user,
                        target=instance.related_object,
                        description=instance.content,
                        actions=actions)

post_save.connect(notify_author, sender=ThreadedComment)

def notify_parent_author(sender, instance, created, **kwargs):
    if instance.parent and created:
        actions = []
        if instance.related_object_type.model == 'tool' or \
           instance.related_object_type.model == 'story':
            href = instance.related_object.get_absolute_url()
            href += '#comment-' + str(instance.id)
            actions.append({
                'title': 'read',
                'href': href
            })
            notify.send(instance.author,
                        verb='replied to your comment',
                        recipient=instance.parent.author,
                        target=instance.parent,
                        description=instance.content,
                        actions=actions)

post_save.connect(notify_parent_author, sender=ThreadedComment)
