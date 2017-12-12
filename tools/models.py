
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete, post_delete, pre_save

from solo.models import SingletonModel
from django_countries.fields import CountryField
from shared.helpers import truncate_string

from common.utils import generate_upload_path


def do_upload_cover_image(inst, filename):
    return generate_upload_path(inst, filename, dirname='cover_images')


def do_upload_suggestion_attachement(inst, filename):
    return generate_upload_path(inst, filename, dirname='suggestions')


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
    categories = models.ManyToManyField('ToolCategory', related_name='tools',
                                        related_query_name='tool')
    published = models.BooleanField(default=False, null=False)
    resources = GenericRelation('resources.ToolResource')

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('tools:show', args=(self.id, ))

    def published_categories(self):
        return self.categories.filter(published=True)

    def sort_tools_descendig(self):
        return self.tools.order_by('-title')


class ToolFollower(models.Model):
    class Meta:
        unique_together = (('user', 'tool'))
        verbose_name = "'Tool Follower"
        verbose_name_plural = 'Tool Followers'

    user = models.ForeignKey('auth.User')
    tool = models.ForeignKey('Tool', related_name='followers')
    should_notify = models.BooleanField(default=False, null=False)


class Story(ModelWithCoverImage):
    class Meta: 
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ('created', )

    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=5000, null=False, blank=False)
    user = models.ForeignKey('auth.User')
    tool = models.ForeignKey('Tool', related_name='stories', blank=True, null=True)
    category_group = models.ForeignKey('CategoryGroup', related_name='stories', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    country = CountryField(blank_label='where did this take place?', null=True)
    associated_tools = models.ManyToManyField(Tool, related_name='associated_tools')

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


class CategoryGroup(models.Model):
    class Meta: 
        verbose_name = 'Work Area'
        verbose_name_plural = 'Work Areas'

    name = models.CharField(max_length=30, null=False, blank=False,
                            unique=True)
    description = models.CharField(max_length=255, blank=True)
    main_text = models.TextField(max_length=5000, blank=True, null=True, default='Lorem ipsum.')
    published = models.BooleanField('published', default=False)
    

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

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
    resources = GenericRelation('resources.ToolResource')
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
    related_content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("tool", "toolcategory")}
    )
    related_object_id = models.PositiveIntegerField(null=False, blank=False)
    related_object = GenericForeignKey('related_content_type',
                                       'related_object_id')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                               blank=False)

    def __str__(self):
        return truncate_string(self.description, 20)

def delete_suggestion_on_related_deleted(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    Suggestion.objects.filter(
        related_content_type__pk=ct.id,
        related_object_id=instance.id
    ).delete()

post_delete.connect(delete_suggestion_on_related_deleted, sender=Tool)
post_delete.connect(delete_suggestion_on_related_deleted, sender=ToolCategory)


class ToolOverviewPage(SingletonModel):
    class Meta: 
        verbose_name = 'Tool Overview Page'

    description = models.CharField(max_length=255, default='Lorem ipsum.')

    class Meta:
        verbose_name = "Tool Overview Page"


class CategoryOverviewPage(SingletonModel):
    class Meta:
        verbose_name = "Toolbox Overview Page"

    description = models.CharField(max_length=255, default='Lorem ipsum.')

    
class CategoryGroupOverviewPage(SingletonModel):
    
    class Meta: 
        verbose_name = "Work Area Overview Page"

    description = models.CharField(max_length=255, default='Lorem ipsum.')
