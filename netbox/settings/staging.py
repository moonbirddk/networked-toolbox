import os
import dj_database_url

from .base import *
from .s3_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
DOMAIN = 'network-toolbox-staging.herokuapp.com'
ALLOWED_HOSTS = [DOMAIN, ]

# We're using S3 for media and static storage.
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_USE_TLS = True
