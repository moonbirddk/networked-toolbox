from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


from common.utils import generate_upload_path


def do_upload_document(inst, filename):
    return generate_upload_path(inst, filename, dirname='resources')


class ToolResourceConnection(models.Model): 
    ## add this as OneToOne to everything that should be able to have resources
    pass


class ToolResource(models.Model):
    title = models.CharField(max_length=60)
    document = models.FileField(upload_to=do_upload_document, blank=False,
                                null=True)
    resource_connection = models.ForeignKey(ToolResourceConnection, on_delete=models.CASCADE, null=True, related_name="resources")
    def __str__(self): 
    	return self.title
