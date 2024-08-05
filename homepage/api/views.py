from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.serializers import ListAllUsersSerializer
from events.api.serializers import AllEventsSerializer
from events.models import Event, EventVideo, EventImage
from news.api.serializers import AllNewsSerializer
from news.models import News
from notifications.models import Notification
from projects.api.serializers import AllProjectsSerializer
from projects.models import Project

User = get_user_model()



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_home_data(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ["User id required"]

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    all_notification = Notification.objects.all().filter(user=user).order_by('-created_at')
    notification_count = all_notification.count()
    data['notification_count'] = notification_count


    users = User.objects.filter(is_archived=False, admin=False)[:10]
    users_serializer = ListAllUsersSerializer(users, many=True)
    data['users'] = users_serializer.data


    all_newss = News.objects.all().filter(is_archived=False)[:10]
    all_newss_serializer = AllNewsSerializer(all_newss, many=True)
    data['newss'] = all_newss_serializer.data


    all_events = Event.objects.all().filter(is_archived=False)[:10]
    all_events_serializer = AllEventsSerializer(all_events, many=True)
    data['events'] = all_events_serializer.data


    all_projects = Project.objects.all().filter(is_archived=False)
    all_projects_serializer = AllProjectsSerializer(all_projects, many=True)
    data['projects'] = all_projects_serializer.data





    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

