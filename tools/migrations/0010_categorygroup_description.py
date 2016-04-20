# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0009_auto_20160322_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorygroup',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
