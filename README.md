Network Toolbox
===============

development
===========
Install postgres database, redis-server and elasticsearch
or use the one from heroku by exporting environment variables.

(No spaces in project path)

```
virtualenv -p python3 .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Subsequent runs:

```
. .venv/bin/activate && ./manage.py migrate && ./manage.py runserver
```

# Setting up the development environment to support task execution

## Get a celery supported broker (in this case Redis)

For ubuntu install the redis-server package

```
sudo apt-get install redis-server
```

And on a new terminal:

```
celery -A netbox worker --concurrency=1 -l debug --purge
```
