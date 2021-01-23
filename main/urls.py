from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from main.views.videos_view import VideosView
# 푸드트럭 urls.py
app_name = 'main'

videos_router = DefaultRouter(trailing_slash=False)
videos_router.register(r'videos', VideosView, basename='videos')

urlpatterns = [
    path('', include(videos_router.urls)),
]
