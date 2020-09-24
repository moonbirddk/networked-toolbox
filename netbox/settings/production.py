import os
from .base import *
import dj_database_url
from .s3_settings import *


DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SITE_ID = 1
DOMAIN = 'www.reflectionaction.org'
ALLOWED_HOSTS = [
    DOMAIN,
    'www.' + DOMAIN,
    'network-toolbox-production.herokuapp.com',
    'networkedtoolbox.com'
]

DATABASES = {
    'default': dj_database_url.config()
}
#DATABASES['default']['ENGINE'] = 'django_postgrespool'
#DATABASES['default']['CONN_MAX_AGE'] = 5
DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEFAULT_FROM_EMAIL = 'Reflection Action <info@{0}>'.format(DOMAIN)
SERVER_EMAIL = 'Reflection Action <alerts@{0}>'.format(DOMAIN)
ADMINS = (
    ('Kræn', 'kraen+network-toolbox-production@socialsquare.dk', ),
    ('Andreas', 'andreas+network-toolbox-production@socialsquare.dk', ),
)
SITE_ADMIN_EMAIL = 'reflectionaction@actionaid.dk'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_USE_TLS = True


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ['BONSAI_URL'],
        'INDEX_NAME': 'haystack',
    },
}
