# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
    # table=None means it is a default! :-)
        migrations.AlterModelTable(
            name='toolresource',
            table=None,
        ),
    ]
