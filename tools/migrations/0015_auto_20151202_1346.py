# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tools', '0014_categoryoverviewpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolresource',
            name='tool',
        ),
        migrations.AddField(
            model_name='toolresource',
            name='content_type',
            field=models.ForeignKey(default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='toolresource',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
