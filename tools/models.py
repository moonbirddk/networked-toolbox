import uuid
from django.db import models
from .utils import generate_upload_path
import os

def do_upload_tool(inst,filename):
     return generate_upload_path(inst, filename, dirname='tools_images')


class Tool(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    cover_image = models.ImageField(upload_to=do_upload_tool, blank=True,
                                    null=True)

class ToolResource(models.Model):
    tool = models.ForeignKey('Tool', null=False, related_name='resources', related_query_name='resource')
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to=do_upload_tool, blank=False,
                                    null=False)

    def css_class(self):
        name, extension = os.path.splitext(self.document.name)

        if extension == '.mp4':
            return 'film'
        if extension == '.jpg':
            return 'picture-o'
        if extension == '.mp3':
            return 'file-audio-o'
        return 'file-text-o'
