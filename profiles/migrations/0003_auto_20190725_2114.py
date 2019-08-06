

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20190725_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='uuid',
        ),
        
    ]
