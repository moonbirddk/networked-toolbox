import os
import dj_database_url

from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
DOMAIN = 'network-toolbox-staging.herokuapp.com'
ALLOWED_HOSTS = [DOMAIN, ]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['ENGINE'] = 'django_postgrespool'
DATABASE_POOL_ARGS = {
    'max_overflow': 2,
    'pool_size': 3,
    'recycle': 300
}

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEFAULT_FROM_EMAIL = 'Info <info@{0}>'.format(DOMAIN)
SERVER_EMAIL = 'Alerts <alerts@{0}>'.format(DOMAIN)

ADMINS = (
    ('Paweł', 'pawel+network-toolbox-staging-heroku@socialsquare.dk',),
    ('Viktor', 'viktor+network-toolbox-staging-heroku@socialsquare.dk',),
)
