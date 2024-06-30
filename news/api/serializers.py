from rest_framework import serializers

from news.models import News
from projects.models import Project


class NewsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"

class AllNewssSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"