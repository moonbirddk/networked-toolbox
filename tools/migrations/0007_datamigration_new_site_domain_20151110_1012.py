# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
#from django.contrib.sites.models import Site


def make_default_site(apps, schema_editor):
    # We can't import the Sites model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Site = apps.get_model("sites", "Site")
    if Site.objects.filter(id=settings.SITE_ID).exists():
        Site.objects.filter(id=settings.SITE_ID)\
            .update(domain=settings.DOMAIN, name=settings.DOMAIN)
    else:
        Site.objects.create(id=settings.SITE_ID, domain=settings.DOMAIN,
                            name=settings.DOMAIN)


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0006_auto_20151104_1313'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_default_site),
    ]
