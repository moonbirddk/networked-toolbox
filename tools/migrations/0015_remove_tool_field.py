# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0014_categoryoverviewpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolresource',
            name='tool',
        ),
        migrations.AddField('ToolResource','object_id', models.PositiveIntegerField(null=True)),
        migrations.AddField('ToolResource','content_type', models.ForeignKey(to='contenttypes.ContentType',null=True)),
    ]
