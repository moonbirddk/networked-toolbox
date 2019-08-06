from django.conf import settings
from django.core.files.storage import default_storage
#
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete, post_delete, pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from comments.models import CommentRoot
from user_notifications.models import NotificationTarget
from resources.models import ToolResourceConnection

from solo.models import SingletonModel
from django_countries.fields import CountryField
from shared.helpers import truncate_string
from shared.db.helpers import get_one_to_one_field_names
from common.utils import generate_upload_path
from user_notifications.signals import notify
from uuid import uuid4


def do_upload_cover_image(inst, filename):
    return generate_upload_path(inst, filename, dirname='cover_images')


def do_upload_suggestion_attachement(inst, filename):
    return generate_upload_path(inst, filename, dirname='suggestions')



class SuggestionRoot(models.Model): 
    # add foreign key to this to any model that should have suggestions
    pass



class ModelWithCoverImage(models.Model):
    class Meta:
        abstract = True

    cover_image = models.ImageField(upload_to=do_upload_cover_image,
                                    blank=True, null=True)

    def has_existing_cover_image(self):
        return self.cover_image and \
            default_storage.exists(self.cover_image.name)

class Tool(ModelWithCoverImage):
    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'
        ordering = ['title']


    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=20000, blank=False)
    resources_text = models.CharField(
        max_length=300,
        default='Here you can find the different resources related to the current tool.',
        blank=True
    )
    categories = models.ManyToManyField('ToolCategory', verbose_name='toolboxes',related_name='tools',
                                        related_query_name='tool')
    published = models.BooleanField(default=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    comment_root = models.OneToOneField('comments.CommentRoot', on_delete=models.CASCADE, null=True)
    resource_connection = models.OneToOneField('resources.ToolResourceConnection',on_delete=models.CASCADE, null=True)
    suggestion_root = models.OneToOneField(SuggestionRoot, on_delete=models.CASCADE, null=True)
    notification_target = models.OneToOneField('user_notifications.NotificationTarget', on_delete=models.CASCADE, null=True)
    
    @property
    def comments(self):
        return self.comment_root.comments.all()

    @property
    def resources(self):
        return self.resource_connection.resources.all()
    
    @property
    def suggestionss(self):
        return self.suggestion_root.suggestions.all()

    def get_absolute_url(self):
        return reverse('tools:show', args=(self.id, ))

    def published_categories(self):
        return self.categories.filter(published=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Tool)
def tool_saved(sender, instance, created, **kwargs): 
    if created:
        suggestion_root = SuggestionRoot()
        comment_root = CommentRoot()
        resource_connection = ToolResourceConnection()
        notification_target = NotificationTarget() 
        suggestion_root.save()
        comment_root.save()
        resource_connection.save()
        notification_target.save()
        instance.suggestion_root = suggestion_root
        instance.comment_root = comment_root
        instance.resource_connection = resource_connection
        instance.notification_target = notification_target
        instance.save()




class ToolFollower(models.Model):
    class Meta:
        unique_together = (('user', 'tool'))
        verbose_name = "'Tool Follower"
        verbose_name_plural = 'Tool Followers'

    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tool = models.ForeignKey('Tool', related_name='followers', on_delete=models.CASCADE)
    should_notify = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '{} - {}'.format(self.user, self.tool)

class ToolUser(models.Model):
    class Meta:
        unique_together = (('user', 'tool'))
        verbose_name = 'Tool User'
        verbose_name_plural = 'Tool Users'

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tool = models.ForeignKey(
        'Tool', related_name='users', on_delete=models.CASCADE)
    should_notify = models.BooleanField(default=False, null=False)


    def __str__(self):
        return '{} - {}'.format(self.user, self.tool)

class Story(ModelWithCoverImage):
    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ('created', )

    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=20000, null=False, blank=False)
    user = models.ForeignKey(
        'auth.User', verbose_name='author', on_delete=models.CASCADE)
    tool = models.ForeignKey('Tool', related_name='stories',
                             blank=True, null=True, on_delete=models.CASCADE)
    category_group = models.ForeignKey('CategoryGroup', verbose_name='work area',
                                       related_name='stories', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    country = CountryField(blank_label='where did this take place?', null=True)
    associated_tools = models.ManyToManyField(Tool, related_name='associated_tools', blank=True)
    published = models.BooleanField('Published', default=True)
    comment_root = models.OneToOneField('comments.CommentRoot', on_delete=models.CASCADE, null=True)
    notification_target = models.OneToOneField(
        'user_notifications.NotificationTarget', on_delete=models.CASCADE, null=True)

    @property
    def comments(self): 
        return self.comment_root.comments.all()

    @property
    def parent_object(self):
        return self.tool if self.tool else self.category_group

    @property
    def parent_object_name(self):
        return self.tool.title if self.tool else self.category_group.name

    def get_absolute_url(self):
        return reverse('tools:show_story', args=(self.id, ))

    def __str__(self):
        return self.title


@receiver(post_save, sender=Tool)
def story_saved(sender, instance, created, **kwargs):
    if created:
        comment_root = CommentRoot()
        notification_target = NotificationTarget()
        comment_root.save()
        notification_target.save()
        instance.comment_root = comment_root
        instance.notification_target = notification_target
        instance.save()



class CategoryGroup(models.Model):
    class Meta:
        verbose_name = 'Work Area'
        verbose_name_plural = 'Work Areas'

    name = models.CharField(max_length=30, null=False, blank=False,
                            unique=True)
    description = models.CharField(max_length=255, blank=True)
    main_text = models.TextField(max_length=5000, blank=True, null=True, default='Lorem ipsum.')
    published = models.BooleanField('published', default=False)
    notification_target = models.OneToOneField(
        'user_notifications.NotificationTarget', on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('tools:show_categorygroup', args=(self.id, ))

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

class CategoryGroupFollower(models.Model):
    class Meta:
        unique_together = (('user', 'category_group'))
        verbose_name = "'Work Area Follower"
        verbose_name_plural = 'Work Area Followers'


    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category_group = models.ForeignKey(
        'CategoryGroup', related_name='followers', on_delete=models.CASCADE)
    should_notify = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '{} - {}'.format(self.user, self.category_group)


def notify_work_area_followers(sender, instance, created, **kwargs):
    CREATED_BIT = {True : 'written'}
    if instance.category_group:
        recipients = CategoryGroupFollower.objects.filter(~Q(user=instance.user), category_group=instance.category_group)
        verb="has {} a story related to a Work Area you follow".format(CREATED_BIT.get(created, 'edited'))
        href = instance.get_absolute_url()
        actions = [{
            'title': 'read',
            'href': href
    
        }]
        email_template = 'stories/email/story_written_about_tool_area'
        for recipient in recipients:
            notify.send(instance.user, verb=verb, recipient=recipient.user, target=instance.category_group, description=instance.title, actions=actions, email_template=email_template)

post_save.connect(notify_work_area_followers, sender=Story)

def get_default_category_group_id(*args, **kwargs):
    return CategoryGroup.objects.get(
        name=settings.DEFAULT_CATEGORY_GROUP_NAME).id


def category_group_check(sender, instance, **kwargs):
    if settings.IN_TEST:
        return
    if instance.name == settings.DEFAULT_CATEGORY_GROUP_NAME:
        raise Exception("Can not update default category group!")
    if instance.id == get_default_category_group_id():
        raise Exception("Can not delete default category group")
pre_delete.connect(category_group_check, sender=CategoryGroup)
pre_save.connect(category_group_check, sender=CategoryGroup)


class ToolCategory(ModelWithCoverImage):
    class Meta:
        verbose_name = 'Toolbox'
        verbose_name_plural = 'Toolboxes'

        ordering = ['order', 'group']

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=20000, blank=False)
    published = models.BooleanField(default=False, null=False)
    resource_connection = models.OneToOneField('resources.ToolResourceConnection', on_delete=models.CASCADE, null=True)
    suggestion_root = models.OneToOneField(SuggestionRoot, null=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, null=False)
    resources_text = models.CharField(
        max_length=300,
        default='Here you can find the different resources'
                ' related to the current category.',
        blank=True
    )
    # A category will belong to only one group; categories not belonging
    # to a group will belong to group 'Other' by default
    group = models.ForeignKey(
        'CategoryGroup',
        null=False,
        default=get_default_category_group_id,
        related_name='categories',
        related_query_name='category',
        on_delete=models.SET_DEFAULT
    )

    @property
    def resources(self):
        return self.resource_connection.resources.all()
    
    @property
    def suggestionss(self):
        return self.suggestion_root.suggestions.all()

    def get_absolute_url(self):
        return reverse('tools:show_category', args=[self.id, ])

    def published_tools(self):
        return self.tools.filter(published=True)

    def __str__(self):
        return "{}".format(self.title)


class Suggestion(models.Model):
    description = models.TextField(max_length=5000, blank=False, null=False)
    attachement = models.FileField(upload_to=do_upload_suggestion_attachement,
                                   blank=True, null=True)
    
    suggestion_root = models.ForeignKey(SuggestionRoot, on_delete=models.CASCADE, null=True, related_name='suggestions')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                               blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return truncate_string(self.description, 20)


class OverviewPage(SingletonModel):
    class Meta:
        abstract = True

    headline = models.CharField(max_length=100, default='Lorem ipsum.')
    description = models.CharField(max_length=255, default='Lorem ipsum.')
    cover_image = models.ImageField(upload_to=do_upload_cover_image,
                                    blank=True, null=True)
    link = models.CharField(max_length=160, default='Loren ipsum.')
    link_text = models.CharField(max_length=40, default='Lorem ipsum.')

    def has_existing_cover_image(self):
        return self.cover_image and \
            default_storage.exists(self.cover_image.name)

class ToolOverviewPage(OverviewPage):
    class Meta:
        verbose_name = 'Tools Overview Page'

class CategoryOverviewPage(OverviewPage):
    class Meta:
        verbose_name = "Toolboxes Overview Page"

class CategoryGroupOverviewPage(OverviewPage):
    class Meta:
        verbose_name = "Work Areas Overview Page"

class StoryOverviewPage(OverviewPage):
    class Meta:
        verbose_name = 'Stories Overview Page'


