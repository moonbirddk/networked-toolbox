import os

django_env = os.getenv('DJANGO_ENV', 'development')

if django_env == 'production':
    from .production import *
elif django_env == 'staging':
    from .staging import *
else:
    from .development import *
