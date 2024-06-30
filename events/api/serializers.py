from rest_framework import serializers

from events.models import Event
from news.models import News
from projects.models import Project


class EventDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"

class AllEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"