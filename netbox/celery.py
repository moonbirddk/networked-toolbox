from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netbox.settings')

from django.conf import settings
from django.utils.importlib import import_module
from celery.utils.log import get_task_logger

app = Celery('netbox')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


log = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(ignore_result=True)
def add(x, y):
    return x + y


@app.task(ignore_result=True)
def clear_expired_sessions():
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        log.error("Session engine '%s' doesn't support clearing "
                  "expired sessions.\n", settings.SESSION_ENGINE)
