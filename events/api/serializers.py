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
    event_images = serializers.SerializerMethodField()
    event_videos = serializers.SerializerMethodField()
    attendees = ListAllUsersSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"

    
    def get_event_images(self, obj):
        # Fetching only the 'photos' field from the Event Images model
        return obj.event_images.filter(is_archived=False).values_list('image', flat=True)


    def get_event_videos(self, obj):
        # Fetching only the 'videos' field from the Event Videos model
        return obj.event_videos.filter(is_archived=False).values_list('video', flat=True)



class AllEventsSerializer(serializers.ModelSerializer):
    event_image = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = "__all__"


    def get_event_image(self, obj):
        event_image = obj.event_images.first()
        if event_image:
            return event_image.image.url
        return None

