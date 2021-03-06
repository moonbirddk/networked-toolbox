# Generated by Django 2.2.8 on 2020-06-25 12:31

from django.db import migrations
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_onlinecourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoresource',
            name='video_file',
            field=library.models.FilerVideoField(on_delete=django.db.models.deletion.CASCADE, related_name='video_resource', to='library.Video', verbose_name='Video file'),
        ),
    ]
