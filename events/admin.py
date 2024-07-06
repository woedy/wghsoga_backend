from django.contrib import admin

from events.models import Event, EventImage, EventVideo

admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventVideo)
