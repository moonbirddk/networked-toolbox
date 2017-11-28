from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


from common.utils import generate_upload_path


def do_upload_document(inst, filename):
    return generate_upload_path(inst, filename, dirname='resources')


class ToolResource(models.Model):
    title = models.CharField(max_length=60)
    document = models.FileField(upload_to=do_upload_document, blank=False,
                                null=False)

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self): 
    	return self.title
