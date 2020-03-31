# Generated by Django 2.2.3 on 2020-03-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_searchbarinfotext_with_highlight'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashTextNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(blank=True, max_length=50, null=True, verbose_name='Headline')),
                ('subtext', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subtext')),
            ],
            options={
                'verbose_name': 'Flash Text',
                'verbose_name_plural': 'Flash Texts',
            },
        ),
        migrations.AlterModelOptions(
            name='flashtext',
            options={'verbose_name': 'Old Flash Text'},
        ),
    ]