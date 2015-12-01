# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0013_tooloverviewpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOverviewPage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255, default='Lorem ipsum.')),
            ],
            options={
                'verbose_name': 'Category Overview Page',
            },
        ),
    ]
