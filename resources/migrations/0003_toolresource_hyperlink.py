# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_add_toolresource_perms_to_admins'),
    ]

    operations = [
        migrations.AddField(
            model_name='toolresource',
            name='hyperlink',
            field=models.CharField(max_length=100, verbose_name='Hyperlink', blank=True, null=True),
        ),
    ]
