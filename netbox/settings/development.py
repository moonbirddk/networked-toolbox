import os
import sys
from .base import *


SECRET_KEY = 'secret key'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
     '--verbosity=2',
     '--with-yanc',
     '--cover-branches',
     '--with-coverage',
     '--cover-erase',
     '--cover-package=netbox',
     '--cover-package=tools',
]

for arg in sys.argv:
    if arg.startswith('--tests='):
        NOSE_ARGS = [
            '--verbosity=2',
            '--stop',
            '--with-yanc',
        ]
        break
