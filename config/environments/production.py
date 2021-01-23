from django.conf import settings
from .base import *
import os

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')