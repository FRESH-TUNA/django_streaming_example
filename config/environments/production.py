from .base import *
from .production_envs import (
    APP_SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
from django.conf import settings
import os

DEBUG = False
SECRET_KEY = APP_SECRET_KEY
ROOT_URLCONF = 'config.urls.production'
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}

from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin
AWS_STORAGE_BUCKET_NAME = "cloudfronttunatest"
AWS_S3_DOMAIN = "https://%s.s3.amazonaws.com" % "cloudfronttunatest/"
AWS_S3_CUSTOM_DOMAIN = "d2ks81gvij7wx9.cloudfront.net"

# Static Setting
STATIC_URL = "https://%s/" % AWS_S3_DOMAIN
STATICFILES_STORAGE = 'config.storages.static_storage.StaticStorage' 

# Media Setting
MEDIA_URL = "https://%s/" % AWS_S3_DOMAIN
DEFAULT_FILE_STORAGE = 'config.storages.media_storage.MediaStorage' 
