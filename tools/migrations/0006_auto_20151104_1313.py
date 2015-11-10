# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0005_toolresource'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to=tools.models.do_upload_cover_image)),
            ],
        ),
        migrations.AddField(
            model_name='tool',
            name='categories',
            field=models.ManyToManyField(related_query_name='tool', related_name='tools', to='tools.ToolCategory'),
        ),
    ]
