# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tools.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0005_add_categorygroup_perms_to_admins'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('cover_image', models.ImageField(null=True, upload_to=tools.models.do_upload_cover_image, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=5000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tool', models.ForeignKey(to='tools.Tool', related_name='stories')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
