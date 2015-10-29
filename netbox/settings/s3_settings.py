import os

# These are the keys for the IAM user
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET')
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'
os.environ['S3_USE_SIGV4'] = 'True'
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
#AWS_S3_CALLING_FORMAT = 2

MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = 'netbox-staging.s3.eu-central-1.amazonaws.com'

### Staticfiles: use Amazon S3
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#S3_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
#STATIC_URL = S3_URL
AWS_PRELOAD_METADATA = True # does this work?
