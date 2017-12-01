# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0014_auto_20160519_1329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'Stories', 'ordering': ('created',), 'verbose_name': 'Story'},
        ),
        migrations.AlterModelOptions(
            name='toolcategory',
            options={'verbose_name_plural': 'Tool Categories', 'ordering': ['order', 'group'], 'verbose_name': 'Tool Category'},
        ),
    ]
