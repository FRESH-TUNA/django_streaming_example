from .base import *
from django.conf import settings
import os

DEBUG = False
ALLOWED_HOST = [os.environ['ALLOWED_HOST']]
ROOT_URLCONF = 'config.urls.production'

SECRET_KEY = os.environ['SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
CLOUDFRONT_URL = os.environ['CLOUDFRONT_URL']
CLOUDFRONT_PRIVATE_KEY = os.environ['CLOUDFRONT_PRIVATE_KEY']
CLOUDFRONT_KEY_PAIR_ID = os.environ['CLOUDFRONT_KEY_PAIR_ID']

from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

AWS_S3_DOMAIN = "https://%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_URL

# Static Setting
STATIC_URL = "https://%s/" % AWS_S3_DOMAIN
STATICFILES_STORAGE = 'config.storages.static_storage.StaticStorage' 

# Media Setting
MEDIA_URL = "https://%s/" % AWS_S3_DOMAIN
DEFAULT_FILE_STORAGE = 'config.storages.media_storage.MediaStorage' 
