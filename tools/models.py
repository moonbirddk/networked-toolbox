import uuid
from django.db import models
from .utils import generate_upload_path


class Tool(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    cover_image = models.ImageField(
        upload_to=lambda inst, filename:
            generate_upload_path(inst, filename, dirname='tools_images'),
        blank=True, null=True)
