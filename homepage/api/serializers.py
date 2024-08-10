from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.models import Event
from news.models import News
from projects.models import Project

User = get_user_model()

class HomeListAllUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["user_id","first_name","last_name","photo",]


class HomeAllEventsSerializer(serializers.ModelSerializer):
    event_image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["event_id", "title", "event_date", "event_image"]

    def get_event_image(self, obj):
        event_image = obj.event_images.first()
        if event_image:
            return event_image.image.url
        return None



class HomeAllNewsSerializer(serializers.ModelSerializer):
    news_image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["news_id", "title", "content", "news_image"]

    def get_news_image(self, obj):
        news_image = obj.news_images.first()
        if news_image:
            return news_image.image.url
        return None



class HomeAllProjectsSerializer(serializers.ModelSerializer):
    project_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["project_id", "title", "details", "project_image"]

    def get_project_image(self, obj):
        project_image = obj.project_images.first()
        if project_image:
            return project_image.image.url
        return None