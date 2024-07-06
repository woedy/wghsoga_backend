from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.api.serializers import AllEventsSerializer, EventDetailsSerializer
from events.models import Event, EventVideo, EventImage

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_event(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        title = request.data.get('title', "")
        theme = request.data.get('theme', "")
        subject = request.data.get('subject', "")
        event_date = request.data.get('event_date', "")
        event_time = request.data.get('event_time', "")
        venue = request.data.get('venue', "")
        organised_by = request.data.get('organised_by', "")

        if not title:
            errors['title'] = ['Title is required.']

        if not theme:
            errors['theme'] = ['Theme is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not event_date:
            errors['event_date'] = ['Event date is required.']

        if not event_time:
            errors['event_time'] = ['Event time is required.']

        if not venue:
            errors['venue'] = ['Venue is required.']

        if not organised_by:
            errors['organised_by'] = ['Organised by is required.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_event = Event.objects.create(
            title=title,
            theme=theme,
            subject=subject,
            event_date=event_date,
            event_time=event_time,
            venue=venue,
            organised_by=organised_by,
        )

        data["event_id"] = new_event.event_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_event_images(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")

        images = request.data.get('images', [])

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            new_image = EventImage.objects.create(
                event=event,
                image=image
            )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_event_videos(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")

        videos = request.data.get('videos', [])

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        for video in videos:
            new_video = EventVideo.objects.create(
                event=event,
                video=video
            )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_events_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_events = Event.objects.all().filter(is_archived=False)

    if search_query:
        all_events = all_events.filter(
            Q(title__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(event_date__icontains=search_query) |
            Q(event_time__icontains=search_query) |
            Q(venue_time__icontains=search_query) |
            Q(organised_by_time__icontains=search_query)
        )

    paginator = Paginator(all_events, page_size)

    try:
        paginated_events = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_events = paginator.page(1)
    except EmptyPage:
        paginated_events = paginator.page(paginator.num_pages)

    all_events_serializer = AllEventsSerializer(paginated_events, many=True)

    data['events'] = all_events_serializer.data
    data['pagination'] = {
        'page_number': paginated_events.number,
        'total_pages': paginator.num_pages,
        'next': paginated_events.next_page_number() if paginated_events.has_next() else None,
        'previous': paginated_events.previous_page_number() if paginated_events.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_event_details_view(request):
    payload = {}
    data = {}
    errors = {}

    event_id = request.query_params.get('event_id', None)

    if not event_id:
        errors['event_id'] = ["Event id required"]

    try:
        event = Event.objects.get(event_id=event_id)
    except:
        errors['event_id'] = ['Event does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    event_serializer = EventDetailsSerializer(event, many=False)
    if event_serializer:
        event = event_serializer.data

    payload['message'] = "Successful"
    payload['data'] = event

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_event(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")
        title = request.data.get('title', "")
        theme = request.data.get('theme', "")
        subject = request.data.get('subject', "")
        event_date = request.data.get('event_date', "")
        event_time = request.data.get('event_time', "")
        venue = request.data.get('venue', "")
        organised_by = request.data.get('organised_by', "")

        if not event_id:
            errors['event_id'] = ['Event ID is required.']

        if not title:
            errors['title'] = ['Title is required.']

        if not theme:
            errors['theme'] = ['Theme is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not event_date:
            errors['event_date'] = ['Event date is required.']

        if not event_time:
            errors['event_time'] = ['Event time is required.']

        if not venue:
            errors['venue'] = ['Venue is required.']

        if not organised_by:
            errors['organised_by'] = ['Organised by is required.']

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event Does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        event.title = title
        event.theme = theme
        event.subject = subject
        event.event_date = event_date
        event.event_time = event_time
        event.venue = venue
        event.organised_by = organised_by
        event.save()

        data["event_id"] = event.event_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_event(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")

        if not event_id:
            errors['event_id'] = ['Event ID is required.']

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        event.is_archived = True
        event.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_event(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")

        if not event_id:
            errors['event_id'] = ['Event ID is required.']

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        event.is_archived = False
        event.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_event(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        event_id = request.data.get('event_id', "")

        if not event_id:
            errors['event_id'] = ['Event ID is required.']

        try:
            event = Event.objects.get(event_id=event_id)
        except:
            errors['event_id'] = ['Event does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        event.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_archived_events_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_events = Event.objects.all().filter(is_archived=True)

    if search_query:
        all_events = all_events.filter(
            Q(title__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(event_date__icontains=search_query) |
            Q(event_time__icontains=search_query) |
            Q(venue_time__icontains=search_query) |
            Q(organised_by_time__icontains=search_query)
        )

    paginator = Paginator(all_events, page_size)

    try:
        paginated_events = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_events = paginator.page(1)
    except EmptyPage:
        paginated_events = paginator.page(paginator.num_pages)

    all_events_serializer = AllEventsSerializer(paginated_events, many=True)

    data['events'] = all_events_serializer.data
    data['pagination'] = {
        'page_number': paginated_events.number,
        'total_pages': paginator.num_pages,
        'next': paginated_events.next_page_number() if paginated_events.has_next() else None,
        'previous': paginated_events.previous_page_number() if paginated_events.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
