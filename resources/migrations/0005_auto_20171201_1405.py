# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20171128_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolresource',
            name='hyperlink',
        ),
        migrations.AlterField(
            model_name='toolresource',
            name='document',
            field=models.FileField(null=True, upload_to=resources.models.do_upload_document),
        ),
    ]
