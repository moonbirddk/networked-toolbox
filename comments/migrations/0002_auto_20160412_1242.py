# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('related_object_id', models.PositiveIntegerField()),
                ('tree_id', models.IntegerField(null=True, db_index=True)),
                ('content', models.TextField(max_length=5000)),
                ('added_dt', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('edited_dt', models.DateTimeField(null=True, auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, blank=True, related_name='children', default=None, to='comments.ThreadedComment')),
                ('related_object_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['tree_id', 'added_dt'],
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='related_object_type',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
