# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0016_categorygroupoverviewpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorygroup',
            name='published',
            field=models.BooleanField(verbose_name='published', default=False),
        ),
    ]
