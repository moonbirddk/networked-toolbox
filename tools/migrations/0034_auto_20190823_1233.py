# Generated by Django 2.2.3 on 2019-08-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20190723_1621'),
        ('tools', '0033_create_comment_relations'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='resource_connection',
            field=models.OneToOneField(
                null=True, on_delete=models.deletion.CASCADE, to='resources.ToolResourceConnection'),
        ),
    ]
