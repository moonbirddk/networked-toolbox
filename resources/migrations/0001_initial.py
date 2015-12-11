# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tools', '0016_move_resources_20151210_1351')
    ]

    state_operations = [
        migrations.CreateModel(
            name='ToolResource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('document', models.FileField(upload_to=resources.models.do_upload_document)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType',null=True)),
            ],
            options={
                'db_table': 'resources_toolresource',
            },
            bases=(models.Model,),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
