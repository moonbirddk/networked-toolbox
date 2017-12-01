# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_toolresource_hyperlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolresource',
            name='document',
            field=models.FileField(upload_to=resources.models.do_upload_document, blank=True, null=True),
        ),
    ]
