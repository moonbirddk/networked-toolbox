from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site

from model_utils.fields import StatusField
from model_utils import Choices
from notifications.models import Notification
from allauth.account.utils import user_email

from tools.models import Story, Tool, ToolFollower
from comments.models import ThreadedComment
from django.urls import reverse

class ActivityEntry(models.Model):
    TYPE_ADD_STORY = 'add_story'
    TYPE_ADD_COMMENT = 'add_comment'
    TYPE_ADD_COMMENT_REPLY = 'add_comment_reply'
    TYPE_USED_TOOL = 'used_tool'
    ENTRY_TYPES = Choices(
            TYPE_ADD_STORY,
            TYPE_ADD_COMMENT,
            TYPE_ADD_COMMENT_REPLY,
            TYPE_USED_TOOL
    )
    user = models.ForeignKey('auth.User')
    entry_type = StatusField(choices_name='ENTRY_TYPES')
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    reverse_url = models.CharField(max_length=100)
    tool_or_story_id = models.IntegerField(default=0)
    hashtag = models.CharField(max_length=25, default='')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def link(self):
        return '{}{}'.format(reverse(self.reverse_url, args=[self.tool_or_story_id]), self.hashtag)
        

@receiver(post_save, sender=Story)
def on_story_create(sender, instance=None, created=False, **kwargs):
    if created:
        related_model = instance.tool if instance.tool else instance.category_group
        print (instance)
        print (related_model)
        link = reverse('tools:show', args=(related_model.id, ))
        link += '#stories'
        ActivityEntry.objects.create(
            user=instance.user,
            entry_type=ActivityEntry.TYPE_ADD_STORY,
            title=related_model.title[:150] if instance.tool else related_model.name[:150],
            content=instance.title,
            link=link
        )


@receiver(post_save, sender=ThreadedComment)
def on_comment_create(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.parent:
            entry_type = ActivityEntry.TYPE_ADD_COMMENT_REPLY
        else:
            entry_type = ActivityEntry.TYPE_ADD_COMMENT

        if hasattr(instance.related_object, 'get_absolute_url'):
            link = instance.related_object.get_absolute_url()
        else:
            raise Error('Expected that the model that was commented on has a'
                        'method to generate an absolute URL.')
        link += '#comment-%d' % instance.id
        title = 'the %s "%s"' % (
            instance.related_object_type.model,
            instance.related_object.title[:150]
        )
        ActivityEntry.objects.create(
            user=instance.author,
            entry_type=entry_type,
            title=title,
            content=instance.content[:500],
            link=link
        )


@receiver(post_save, sender=ToolFollower)
def on_tool_used(sender, instance=None, created=False, **kwargs):
    if created:
        link = reverse('tools:show', args=(instance.tool.id, ))
        ActivityEntry.objects.create(
            user=instance.user,
            entry_type=ActivityEntry.TYPE_USED_TOOL,
            title=instance.tool.title[:150],
            link=link
        )

# Send notifications as mail if they have an email_template associated
@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance=None, created=False, **kwargs):
    import pdb
    if not created: 
        return
    email_template = None
    if instance.data: 
        email_template = instance.data.get('email_template')
    if email_template:
        context = {
            'user': instance.recipient,
            'actor': instance.actor,
            'verb': instance.verb,
            'target': instance.target,
            'description': instance.description,
            'BASE_URL': 'http://%s' % Site.objects.get_current().domain
        }
        # Add the notification data to the context
        context.update(instance.data)
        # Render the subject and message templates
        subject_template = '%s_subject.txt' % email_template
        message_template = '%s_message.txt' % email_template
        subject = render_to_string(subject_template, context)
        message = render_to_string(message_template, context)
        subject = " ".join(subject.splitlines()).strip()
        # Send the mail
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email(instance.recipient)]
        )

# Inject a better __str__ method on the Django User class
User.add_to_class("__str__", User.get_full_name)
