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
from homepage.api.serializers import HomeListAllUsersSerializer, HomeAllEventsSerializer, HomeAllProjectsSerializer, \
    HomeAllNewsSerializer
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

    print("###################")
    print(user_id)

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

    user_data = {
        'first_name': user.first_name,
        'photo': user.photo.url,
        'year_group': user.year_group,
    }
    data['user_data'] = user_data

    all_notification = Notification.objects.all().filter(user=user).filter(read=False).order_by('-created_at')

    if all_notification.count() > 0:
        data['notification'] = True
    else:
        data['notification'] = False
#
#
    users = User.objects.filter(is_archived=False, admin=False, verified=True).order_by('-timestamp')[:10]
    #users = User.objects.filter(is_archived=False, admin=False, year_group=user.year_group)[:10]
    users_serializer = HomeListAllUsersSerializer(users, many=True)
    data['users'] = users_serializer.data
#
#
    all_newss = News.objects.all().filter(is_archived=False, draft=False).order_by('-created_at')[:10]
    all_newss_serializer = HomeAllNewsSerializer(all_newss, many=True)
    data['news'] = all_newss_serializer.data
#
#
    all_events = Event.objects.all().filter(is_archived=False, draft=False).order_by('-created_at')[:10]
    all_events_serializer = HomeAllEventsSerializer(all_events, many=True)
    data['events'] = all_events_serializer.data
#
#
    all_projects = Project.objects.all().filter(is_archived=False, draft=False).order_by('-created_at')[:10]
    all_projects_serializer = HomeAllProjectsSerializer(all_projects, many=True)
    data['projects'] = all_projects_serializer.data





    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_dashboard_data(request):
    payload = {}
    data = {}
    errors = {}

    users_count = User.objects.filter(is_archived=False).count()
    data['users_count'] = users_count
    all_newss_count = News.objects.all().filter(is_archived=False).count()
    data['news_count'] = all_newss_count
    all_events_count = Event.objects.all().filter(is_archived=False).count()
    data['events_count'] = all_events_count
    all_projects_count = Project.objects.all().filter(is_archived=False).count()
    data['projects_count'] = all_projects_count


#
    users = User.objects.filter(is_archived=False).order_by('-timestamp')[:5]
    #users = User.objects.filter(is_archived=False, admin=False, year_group=user.year_group)[:10]
    users_serializer = ListAllUsersSerializer(users, many=True)
    data['users'] = users_serializer.data
#
#
    all_newss = News.objects.all().filter(is_archived=False).order_by('-created_at')[:5]
    all_newss_serializer = AllNewsSerializer(all_newss, many=True)
    data['news'] = all_newss_serializer.data
#
#
    all_events = Event.objects.all().filter(is_archived=False).order_by('-created_at')[:5]
    all_events_serializer = AllEventsSerializer(all_events, many=True)
    data['events'] = all_events_serializer.data
#
#
    all_projects = Project.objects.all().filter(is_archived=False).order_by('-created_at')[:10]
    all_projects_serializer = AllProjectsSerializer(all_projects, many=True)
    data['projects'] = all_projects_serializer.data





    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

