# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tools.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryOverviewPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.CharField(max_length=255, default='Lorem ipsum.')),
            ],
            options={
                'verbose_name': 'Category Overview Page',
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.TextField(max_length=5000)),
                ('attachement', models.FileField(blank=True, upload_to=tools.models.do_upload_suggestion_attachement, null=True)),
                ('related_object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('related_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('cover_image', models.ImageField(blank=True, upload_to=tools.models.do_upload_cover_image, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('resources_text', models.CharField(max_length=300, blank=True, default='Here you can find the different resources related to the current tool.')),
                ('published', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ToolCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('cover_image', models.ImageField(blank=True, upload_to=tools.models.do_upload_cover_image, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('published', models.BooleanField(default=False)),
                ('resources_text', models.CharField(max_length=300, blank=True, default='Here you can find the different resources related to the current category.')),
                ('group', models.ForeignKey(related_name='categories', on_delete=django.db.models.deletion.SET_DEFAULT, to='tools.CategoryGroup', default=tools.models.get_default_category_group_id, related_query_name='category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ToolFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('should_notify', models.BooleanField(default=False)),
                ('tool', models.ForeignKey(to='tools.Tool', related_name='followers')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ToolOverviewPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', models.CharField(max_length=255, default='Lorem ipsum.')),
            ],
            options={
                'verbose_name': 'Tool Overview Page',
            },
        ),
        migrations.AddField(
            model_name='tool',
            name='categories',
            field=models.ManyToManyField(related_name='tools', related_query_name='tool', to='tools.ToolCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='toolfollower',
            unique_together=set([('user', 'tool')]),
        ),
    ]
