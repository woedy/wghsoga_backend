from rest_framework import serializers

from accounts.api.serializers import ListAllUsersSerializer
from events.models import Event, EventImage, EventVideo


class EventVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventVideo
        fields = "__all__"


class EventImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventImage
        fields = "__all__"

class EventDetailsSerializer(serializers.ModelSerializer):
    event_images = EventImageSerializer(many=True)
    event_videos = EventVideoSerializer(many=True)
    attendees = ListAllUsersSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"

class AllEventsSerializer(serializers.ModelSerializer):
    event_images = EventImageSerializer(many=True)
    event_videos = EventVideoSerializer(many=True)
    attendees = ListAllUsersSerializer(many=True)
    class Meta:
        model = Event
        fields = "__all__"