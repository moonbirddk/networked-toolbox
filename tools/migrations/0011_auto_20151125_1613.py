# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0010_suggestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toolcategory',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
