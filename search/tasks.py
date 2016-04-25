from __future__ import absolute_import


from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.importlib import import_module

from django.core.management import call_command


log = get_task_logger(__name__)


@shared_task(ignore_result=True)
def rebuild_index():
    log.info("rebuilding index...")
    call_command('rebuild_index', noinput=True, interactive=False)
    log.info("rebuilding index DONE.")
