from .base import *
from django.conf import settings
import os

DEBUG = False
ALLOWED_HOSTS = [os.environ['ALLOWED_HOST']]
ROOT_URLCONF = 'config.urls.production'

SECRET_KEY = os.environ['SECRET_KEY']
