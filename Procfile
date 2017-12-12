web: newrelic-admin run-program gunicorn netbox.wsgi:application --env DJANGO_SETTINGS_MODULE=netbox.settings --log-file -
celery_worker: newrelic-admin run-program celery -A netbox worker --concurrency=1 -l info
celery_beat: newrelic-admin run-program celery -A netbox beat