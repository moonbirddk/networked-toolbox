# Generated by Django 2.2.8 on 2020-03-20 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20200316_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashtextnew',
            name='subtext',
            field=models.CharField(default='', max_length=200, verbose_name='Subtext'),
        ),
    ]