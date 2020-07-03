# Generated by Django 2.2.8 on 2020-07-03 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0011_auto_20200703_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinecourse',
            name='participiants',
            field=models.ManyToManyField(related_name='participiants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CourseFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('should_notify', models.BooleanField(default=True)),
                ('online_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='library.OnlineCourse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]