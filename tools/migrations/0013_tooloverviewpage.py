# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0012_auto_20151130_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolOverviewPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(max_length=255, default='Lorem ipsum.')),
            ],
            options={
                'verbose_name': 'Tool Overview Page',
            },
        ),
    ]
