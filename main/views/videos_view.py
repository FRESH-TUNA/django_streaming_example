from django.shortcuts import redirect, reverse
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import mixins
from main.permissions import OnlyList
from layout.views import BaseModelViewSet

class VideosView(BaseModelViewSet):
    permission_classes = [OnlyList]
    pass
