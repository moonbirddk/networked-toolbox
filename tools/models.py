
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete

from solo.models import SingletonModel

from common.utils import generate_upload_path


def do_upload_cover_image(inst, filename):
    return generate_upload_path(inst, filename, dirname='cover_images')


def do_upload_document(inst, filename):
    return generate_upload_path(inst, filename, dirname='resources')


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
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    categories = models.ManyToManyField('ToolCategory', related_name='tools',
                                        related_query_name='tool')
    published = models.BooleanField(default=False, null=False)

    def get_absolute_url(self):
        return reverse('tools:show', args=[self.id, ])

    def published_categories(self):
        return self.categories.filter(published=True)


class ToolFollower(models.Model):
    class Meta:
        unique_together = (('user', 'tool'))
    user = models.ForeignKey('auth.User')
    tool = models.ForeignKey('Tool', related_name='followers')
    should_notify = models.BooleanField(default=False, null=False)


class ToolResource(models.Model):
    tool = models.ForeignKey(
        'Tool',
        null=False,
        related_name='resources',
        related_query_name='resource'
    )
    title = models.CharField(max_length=60)
    document = models.FileField(upload_to=do_upload_document, blank=False,
                                null=False)


class ToolCategory(ModelWithCoverImage):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    published = models.BooleanField(default=False, null=False)

    def get_absolute_url(self):
        return reverse('tools:show_category', args=[self.id, ])

    def published_tools(self):
        return self.tools.filter(published=True)


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


def delete_suggestion_on_related_deleted(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(sender)
    Suggestion.objects.filter(
        related_content_type__pk=ct.id,
        related_object_id=instance.id
    ).delete()

post_delete.connect(delete_suggestion_on_related_deleted, sender=Tool)
post_delete.connect(delete_suggestion_on_related_deleted, sender=ToolCategory)

class ToolOverviewPage(SingletonModel):
    description = models.CharField(max_length=255, default='Lorem ipsum.')

    class Meta:
        verbose_name = "Tool Overview Page"


class CategoryOverviewPage(SingletonModel):
    description = models.CharField(max_length=255, default='Lorem ipsum.')

    class Meta:
        verbose_name = "Category Overview Page"
