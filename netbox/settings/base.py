"""
Django settings for netbox project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import datetime
from celery.schedules import crontab

SITE_ID = 1
DOMAIN = 'localhost'
DEFAULT_FROM_EMAIL = 'Networked Toolbox <hello@{}>'.format(DOMAIN)
SITE_ADMIN_EMAIL = 'admin@{}'.format(DOMAIN)

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.join(BASE_DIR, 'netbox')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ns9#tfv!^k*=$5e+9-n5(er(8zxw9y(5gi_^s#-#h^(s$83a_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = False

ALLOWED_HOSTS = []

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_gulp',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'bootstrap3',
    'storages',
    'django_summernote',
    'solo',
    'django_countries',
    'compressor',
    'easy_timezones',
    'haystack',

    'common',
    'profiles',
    'tools',
    'resources',
    'comments',
    'search',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'easy_timezones.middleware.EasyTimezoneMiddleware',

    'netbox.middleware.RedirectToTermsAndConditionsMiddleware',

)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'netbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "netbox.context_processors.timezone_name",
            ],
        },
    },
]

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Change editor size
    'width': '100%',
    'height': '480',

    # Use proper language setting automatically (default)
    'lang': None,

    'toolbar': [
        ['group', [ 'fontstyle' ]],
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['insert', ['link', 'picture','video']],
        ['view', ['fullscreen']],
        ['help', ['help']]
    ],

    'fontNames': [
        'American Typewriter'
    ],
    # Need authentication while uploading attachments.
    'attachment_require_authentication': False,

    # Set external media files for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'inplacewidget_external_css': (
       # '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
        #'//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (
        #'//code.jquery.com/jquery-1.9.1.min.js',
        #'//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
}

WSGI_APPLICATION = 'netbox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL_PATTERN = '/static/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL_PATTERN = "/media/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Network Toolbox]"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_DISPLAY = lambda user: user.email
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_SESSION_REMEMBER = None
SITE_OPEN_FOR_SIGNUP = True
LOGOUT_URL = 'account_logout'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'tools:index'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_PROVIDERS = {
'facebook': {
    'METHOD': 'oauth2',
    'SCOPE': ['email', 'public_profile', 'user_friends'],
    'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    'FIELDS': [
        'id',
        'email',
        'name',
        'first_name',
        'last_name',
        'verified',
        'locale',
        'timezone',
        'link',
        'gender',
        'updated_time'],
    'EXCHANGE_TOKEN': True,
    #'LOCALE_FUNC': 'path.to.callable',
    'VERIFIED_EMAIL': False,
    'VERSION': 'v2.4'
    },
}

IN_TEST = 'test' in sys.argv
DEFAULT_CATEGORY_GROUP_NAME = 'Other'
COMPRESS_ENABLED = False
COMMENT_MAX_LENGTH = 5000
COMMENT_READ_MORE_LENGTH = 500


GEOIP_DATABASE = os.path.join(BASE_DIR, 'geoip/GeoLiteCity.dat')
GEOIPV6_DATABASE = os.path.join(BASE_DIR, 'geoip/GeoLiteCityv6.dat')

SEARCH_NUM_RESULTS = 4

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#        'URL': 'http://127.0.0.1:9200/',
#        'INDEX_NAME': 'haystack',
#    },
#}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

BROKER_URL = os.environ.get('REDIS_URL', 'redis://')
CELERY_IGNORE_RESULT = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
if 'test' in sys.argv:
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    CELERY_ALWAYS_EAGER = True
    BROKER_BACKEND = 'memory'

CELERYBEAT_SCHEDULE = {
    'clear-sessions-everyday-at-1-30': {
        'task': 'netbox.celery.clear_expired_sessions',
        'schedule': crontab(hour=1, minute=30),
    },
    'rebuild-index-everyday-at-2-30': {
        'task': 'search.tasks.rebuild_index',
        'schedule': crontab(hour=2, minute=30),
    },
}
