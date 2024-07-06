from django.urls import path

from events.api.views import add_event, edit_event, get_all_events_view, get_event_details_view, archive_event, \
    delete_event, unarchive_event, get_all_archived_events_view, add_event_images, add_event_videos

app_name = 'events'

urlpatterns = [
    path('add-event/', add_event, name="add_event"),
    path('add-event-images/', add_event_images, name="add_event_images"),
    path('add-event-videos/', add_event_videos, name="add_event_videos"),
    path('edit-event/', edit_event, name="edit_event"),
    path('get-all-events/', get_all_events_view, name="get_all_events_view"),
    path('get-event-details/', get_event_details_view, name="get_event_details_view"),
    path('archive-event/', archive_event, name="archive_event"),
    path('delete-event/', delete_event, name="delete_event"),
    path('unarchive-event/', unarchive_event, name="unarchive_event"),
    path('get-all-archived-events/', get_all_archived_events_view, name="get_all_archived_events_view"),

]
