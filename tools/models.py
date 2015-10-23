from django.db import models
from django.conf import settings

# Create your models here.
class Tool(models.Model):
    title=models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    cover_image = models.ImageField(upload_to= settings.MEDIA_ROOT + '/tools_images', blank=True, null=True)