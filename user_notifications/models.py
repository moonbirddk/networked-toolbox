# -*- coding: utf-8 -*-
from django import get_version
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.six import text_type
from jsonfield.fields import JSONField
from model_utils import Choices

from user_notifications import settings as notifications_settings
from user_notifications.signals import notify
from user_notifications.utils import id2slug
from swapper import load_model, swappable_setting


# THIS IS A CLONE OF https://github.com/django-notifications
# to work without generic foreign keys and to make networked_toolbox more maintainable
# by getting rid of a depencency

EXTRA_DATA = notifications_settings.get_config()['USE_JSONFIELD']


def is_soft_delete():
    return notifications_settings.get_config()['SOFT_DELETE']


def assert_soft_delete():
    if not is_soft_delete():
        # msg = """To use 'deleted' field, please set 'SOFT_DELETE'=True in settings.
        # Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
        # """
        msg = 'REVERTME'
        raise ImproperlyConfigured(msg)


class NotificationQuerySet(models.query.QuerySet):
    ''' Notification QuerySet '''

    def unsent(self):
        return self.filter(emailed=False)

    def sent(self):
        return self.filter(emailed=True)

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=True, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=True)

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=False, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qset = self.unread(True)
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        qset = self.read(True)

        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=True)

    def deleted(self):
        """Return only deleted items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=True)

    def active(self):
        """Return only active(un-deleted) items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        """Mark current queryset as deleted.
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.active()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=True)

    def mark_all_as_active(self, recipient=None):
        """Mark current queryset as active(un-deleted).
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.deleted()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=False)

    def mark_as_unsent(self, recipient=None):
        qset = self.sent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=False)

    def mark_as_sent(self, recipient=None):
        qset = self.unsent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.updat

class NotificationTarget(models.Model): 
    pass
    ## Add this as OneToOneField to everything that can be a notification target
    ## stories, tools, workareas, comments as of now

class AbstractNotification(models.Model):

    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(
        choices=LEVELS, default=LEVELS.info, max_length=20)

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='received_notifications',
        on_delete=models.CASCADE
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True)

    # The only actor is a user, thus code change 
    
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='sent_notifications',
        on_delete=models.CASCADE
    )

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # notification targets can be stories, tools, workareas, comments
    target_connection = models.ForeignKey(NotificationTarget, on_delete=models.CASCADE, null=True, related_name='notifications')

    # Omitting action object
    
    @property 
    def target(self): 
        if hasattr(self.target_connection, 'story'): 
            return self.target_connection.story
        elif hasattr(self.target_connection,'tool'): 
            return self.target_connection.tool
        elif hasattr(self.target_connection, 'categorygroup'):
            return self.target_connection.categorygroup
        else:
            return self.target_connection.threadedcomment
        
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    public = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)

    data = JSONField(blank=True, null=True)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ('-timestamp',)
        app_label = 'user_notifications'
        # speed up notifications count query
        index_together = ('recipient', 'unread')

    def __str__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
           return '{} {} {} {} ago'.format(
               ctx['actor'], 
               ctx['verb'], 
               ctx['target'], 
               ctx['timesince'], 
           )
    
        return '{} {} {} ago'.format(
            ctx['actor'], 
            ctx['verb'], 
            ctx['timesince'], 
        )

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target', 'action_object')
    ]
    public = bool(kwargs.pop('public', True))
    description = kwargs.pop('description', None)
    timestamp = kwargs.pop('timestamp', timezone.now())
    UserNotification = load_model('user_notifications', 'UserNotification')
    level = kwargs.pop('level', UserNotification.LEVELS.info)

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    for recipient in recipients:
       
        newnotify = UserNotification(
            recipient=recipient,
            actor=actor,
            verb=text_type(verb),
            public=public,
            description=description,
            timestamp=timestamp,
            level=level,
        )
        for obj, opt in optional_objs:
            if obj is not None:
                newnotify.target_connection = obj.notification_target

        if kwargs and EXTRA_DATA:
            newnotify.data = kwargs

        newnotify.save()
        new_notifications.append(newnotify)

    return new_notifications


#connect the signal
notify.connect(
   notify_handler, dispatch_uid='user_notifications.models.UserNotification')


class UserNotification(AbstractNotification):

    class Meta(AbstractNotification.Meta):
        abstract = False
        swappable = swappable_setting('user_notifications', 'UserNotification')
