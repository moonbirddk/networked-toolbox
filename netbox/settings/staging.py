import os
import dj_database_url

from .base import *
from .s3_settings import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SITE_ID = 1
DOMAIN = 'network-toolbox-staging.herokuapp.com'
ALLOWED_HOSTS = [DOMAIN, ]

# We're using S3 for media and static storage.
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['ENGINE'] = 'django_postgrespool'
#DATABASES['default']['CONN_MAX_AGE'] = 5
DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}

SECRET_KEY = '1d427e2f01b46d5ae6188c42e55b0956'

DEFAULT_FROM_EMAIL = 'Networked Toolbox <info@{0}>'.format(DOMAIN)
SERVER_EMAIL = 'Networked Toolbox <alerts@{0}>'.format(DOMAIN)

ADMINS = (
    ('Kræn', 'kraen+network-toolbox-staging@socialsquare.dk', ),
    ('Andreas', 'andreas+network-toolbox-staging@socialsquare.dk', ),
)
SITE_ADMIN_EMAIL = 'networkedtoolbox@actionaid.dk'

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

GOOGLE_ANALYTICS_ID = 'UA-71138728-2'
