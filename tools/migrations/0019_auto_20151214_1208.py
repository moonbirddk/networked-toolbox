# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0018_tool_resources_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolcategory',
            name='resources_text',
            field=models.CharField(max_length=300, default='Here you can find the different resources related to the current category.'),
        ),
    ]
