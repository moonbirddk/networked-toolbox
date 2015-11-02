# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tools.models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_auto_20151028_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolResource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('document', models.FileField(upload_to=tools.models.do_upload_tool)),
                ('tool', models.ForeignKey(to='tools.Tool', related_query_name='resource', related_name='resources')),
            ],
        ),
    ]
