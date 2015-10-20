import os
from .base import *

django_env = os.getenv('DJANGO_ENV')

if django_env == 'production':
    from .production import *
elif django_env == 'staging':
    from .staging import *
