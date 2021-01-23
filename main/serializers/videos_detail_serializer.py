from rest_framework import serializers
from main.models import Video

class VideosDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
