# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0008_story_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='description',
            field=models.TextField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='toolcategory',
            name='description',
            field=models.TextField(max_length=20000),
        ),
    ]
