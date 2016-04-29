Network Toolbox
===============

development
===========
   install postgres database, redis-server and elasticsearch
   or use the one from heroku by exporting environment variables.
   
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    npm install
    export DJANGO_SETTINGS_MODULE=netbox.settings
    ./manage.py migrate
    ./manage/py runserver
