
from django.db import models
from django.core.files.storage import default_storage

from .utils import generate_upload_path


def do_upload_cover_image(inst, filename):
    return generate_upload_path(inst, filename, dirname='cover_images')


def do_upload_document(inst, filename):
    return generate_upload_path(inst, filename, dirname='resources')


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


class ToolResource(models.Model):
    tool = models.ForeignKey(
        'Tool',
        null=False,
        related_name='resources',
        related_query_name='resource'
    )
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to=do_upload_document, blank=False,
                                null=False)


class ToolCategory(ModelWithCoverImage):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
