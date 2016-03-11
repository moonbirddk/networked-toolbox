Network Toolbox
===============

development
===========
    
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    export DJANGO_SETTINGS_MODULE=netbox.settings
    ./manage.py migrate
    ./manage/py runserver
