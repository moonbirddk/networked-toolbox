from django.db import models

# Create your models here.
class Tool(models.Model):
    title=models.CharField(max_length=30)
    description = models.CharField(max_length=5000)