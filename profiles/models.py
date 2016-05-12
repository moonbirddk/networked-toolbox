import uuid
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.core.urlresolvers import reverse

from django_countries.fields import CountryField

from common.utils import generate_upload_path

from model_utils.fields import StatusField
from model_utils import Choices

from tools.models import Tool, Story
from comments.models import ThreadedComment


def do_upload_profile_photo(inst, filename):
    return generate_upload_path(inst, filename, dirname='profile_photos')


def generate_profile_uid():
    return uuid.uuid4().hex


PROFILE_BIO_MAX_LEN = 400


class ProfileManager(models.Manager):
    def create(self, *args, **kwargs):
        kwargs['uid'] = generate_profile_uid()
        return super().create(*args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        with transaction.atomic():
            qs = self.get_queryset().filter(*args, **kwargs)
            if not qs.count():
                return self.create(*args, **kwargs), True
            return qs.first(), False


class Profile(models.Model):
    uid = models.CharField(unique=True, editable=False, null=True,
                           max_length=32)
    # FIXME: migrate uid to be not null
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to=do_upload_profile_photo,
                              blank=True, null=True)
    bio = models.TextField(
        max_length=PROFILE_BIO_MAX_LEN,
        blank=True,
        null=True
    )
    country = CountryField(blank_label='where did this take place?',
                           blank=True, null=True)

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_profile_uid()
        return super().save(*args, **kwargs)

    def name(self):
        user = self.user
        if user.first_name and user.last_name:
            return "{} {}".format(user.first_name, user.last_name)
        elif user.first_name:
            return user.first_name
        elif user.last_name:
            return user.last_name
        else:
            return "Noname Nosurname"

    def short_name(self):
        user = self.user
        if user.first_name and user.last_name:
            last_name = user.last_name[0] + '.'
            return "{} {}".format(user.first_name, last_name)
        elif user.first_name:
            return user.first_name
        else:
            return user.last_name

    def has_existing_photo(self):
        return self.photo and \
            default_storage.exists(self.photo.name)

    def get_absolute_url(self):
        return reverse('profiles:show', args=(self.uid, ))


@receiver(post_save, sender=User, dispatch_uid='profiles-create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile, dispatch_uid="profiles-on_profile_pre_save")
def on_profile_pre_save(sender, instance, **kwargs):
    try:
        old = Profile.objects.get(id=instance.id)
    except Profile.DoesNotExist:
        return

    if old.photo and old.photo.name and old.photo != instance.photo and\
            default_storage.exists(old.photo.name):
        default_storage.delete(old.photo.name)


@receiver(post_delete, sender=Profile,
          dispatch_uid="profiles-on_profile_post_delete")
def on_profile_post_delete(sender, instance, **kwargs):
    if instance.photo and instance.photo.name and\
            default_storage.exists(instance.photo.name):
        default_storage.delete(instance.photo.name)

class ActivityEntry(models.Model):
    TYPE_ADD_STORY = 'add_story'
    TYPE_ADD_COMMENT = 'add_comment'
    TYPE_ADD_COMMENT_REPLY = 'add_comment_reply'
    ENTRY_TYPES = Choices(
            TYPE_ADD_STORY,
            TYPE_ADD_COMMENT,
            TYPE_ADD_COMMENT_REPLY
    )
    user = models.ForeignKey('auth.User')
    entry_type = StatusField(choices_name='ENTRY_TYPES')
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    link = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Story)
def on_story_create(sender, instance=None, created=False, **kwargs):
    if created:
        link = reverse('tools:show', args=(instance.tool.id, ))
        ActivityEntry.objects.create(user=instance.user,
                entry_type=ActivityEntry.TYPE_ADD_STORY, title=instance.tool.title,
                content=instance.content, link=link)

@receiver(post_save, sender=ThreadedComment)
def on_comment_create(sender, instance=None, created=False, **kwargs):
    if not created: return

    view = isinstance(instance.related_object, Tool) and 'tools:show'\
            or 'tools:show_story'
    entry_type = instance.parent and ActivityEntry.TYPE_ADD_COMMENT_REPLY\
            or ActivityEntry.TYPE_ADD_COMMENT

    link = reverse(view, args=(instance.related_object.id, ))
    ActivityEntry.objects.create(user=instance.author,
            entry_type=entry_type,
            title=instance.related_object.title,
            content=instance.content, link=link)
