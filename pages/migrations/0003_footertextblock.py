# Generated by Django 2.2.3 on 2019-10-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_flashtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterTextblock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(default='Contact the team', max_length=50, verbose_name='Headline')),
                ('body', models.TextField(default='To get in touch with the team behind Networked Toolbox, drop us an e-mail at: ', max_length=200, verbose_name='Body')),
                ('contact_mail', models.EmailField(default='networkedtoolbox@ms.dk', max_length=254, verbose_name='Contact address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]