from rest_framework import serializers
from main.models import Video

class VideosListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='main:videos-detail')

    class Meta:
        model = Video
        fields = '__all__'
