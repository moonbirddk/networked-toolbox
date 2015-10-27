# From: http://stackoverflow.com/a/10825691/118608
from storages.backends.s3 import S3Storage
STATIC_PREPENDED_S3_STORAGE = lambda: S3Storage(location='static')
MEDIA_PREPENDED_S3_STORAGE = lambda: S3Storage(location='media')