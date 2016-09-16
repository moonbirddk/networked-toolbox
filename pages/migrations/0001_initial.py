# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
            ],
        ),
    ]
