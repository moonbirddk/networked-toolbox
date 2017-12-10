# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0020_remove_categorygroup_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorygroup',
            name='published',
            field=models.BooleanField(verbose_name='published', default=False),
        ),
    ]
