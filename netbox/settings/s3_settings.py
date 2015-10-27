import os

#from S3 import CallingFormat
#AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

AWS_CALLING_FORMAT = 2

### Configure S3
# These are the keys for the IAM user `django_s3_user` on AWS
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET')


### Media files (uploads): use Amazon S3
DEFAULT_FILE_STORAGE = 'netbox.s3_utils.MEDIA_PREPENDED_S3_STORAGE'
MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

### Staticfiles: use Amazon S3
STATICFILES_STORAGE = 'netbox.s3_utils.STATIC_PREPENDED_S3_STORAGE'
S3_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
AWS_PRELOAD_METADATA = True # Only upload new files (doesn't actually work)
                            # we use "github.com/antonagestam/collectfast"
                            # in order to only upload new/updated files