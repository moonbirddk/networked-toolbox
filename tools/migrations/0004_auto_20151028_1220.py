# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_auto_20151023_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=tools.models.do_upload_cover_image),
        ),
        migrations.AlterField(
            model_name='tool',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
