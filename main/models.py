from layout.models import TimeStampedModel
from django.db import models

class Video(TimeStampedModel):
    url = models.FileField(upload_to=None, max_length=100)
