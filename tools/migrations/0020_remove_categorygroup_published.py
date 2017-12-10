# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0019_auto_20171204_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorygroup',
            name='published',
        ),
    ]
