Network Toolbox
===============

development
===========
    
    virtualenv venv
    . venv/bin/activate
    export DJANGO_SETTINGS_MODULE=netbox.settings_superduper.py
    ./manage.py syncdb
    ./manage.py migrate
    ./manage/py runserver
