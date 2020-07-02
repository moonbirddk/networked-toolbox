# Generated by Django 2.2.8 on 2020-05-25 07:58

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20200525_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarydocument',
            name='cover_image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_cover_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Cover Image'),
        ),
    ]
