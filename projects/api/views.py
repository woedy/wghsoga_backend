from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.api.serializers import AllProjectsSerializer, ProjectDetailsSerializer
from projects.models import Project, ProjectImage, ProjectVideo


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_project(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        title = request.data.get('title', "")
        details = request.data.get('details', "")
        target = request.data.get('target', "")

        if not title:
            errors['title'] = ['Title is required.']

        if not details:
            errors['details'] = ['Details is required.']

        if not target:
            errors['target'] = ['Target is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        new_project = Project.objects.create(
            title=title,
            details=details,
            target=target,

        )

        data["project_id"] = new_project.project_id



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_project_images(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")


        images = request.data.get('images', [])

        try:
           project = Project.objects.get(project_id=project_id)
        except:
           errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        for image in images:
            new_image = ProjectImage.objects.create(
                project=project,
                image=image
            )


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_project_videos(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")


        videos = request.data.get('videos', [])

        try:
           project = Project.objects.get(project_id=project_id)
        except:
           errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        for video in videos:
            new_video = ProjectVideo.objects.create(
                project=project,
                video=video
            )


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_projects_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_projects = Project.objects.all().filter(is_archived=False)


    if search_query:
        all_projects = all_projects.filter(
            Q(title__icontains=search_query) |
            Q(detail_name__icontains=search_query) |
            Q(target__username__icontains=search_query)
        )


    paginator = Paginator(all_projects, page_size)

    try:
        paginated_projects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_projects = paginator.page(1)
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)

    all_projects_serializer = AllProjectsSerializer(paginated_projects, many=True)


    data['projects'] = all_projects_serializer.data
    data['pagination'] = {
        'page_number': paginated_projects.number,
        'total_pages': paginator.num_pages,
        'next': paginated_projects.next_page_number() if paginated_projects.has_next() else None,
        'previous': paginated_projects.previous_page_number() if paginated_projects.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)







@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_project_details_view(request):
    payload = {}
    data = {}
    errors = {}

    project_id = request.query_params.get('project_id', None)

    if not project_id:
        errors['project_id'] = ["Project id required"]

    try:
        project = Project.objects.get(project_id=project_id)
    except:
        errors['project_id'] = ['Project does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    project_serializer = ProjectDetailsSerializer(project, many=False)
    if project_serializer:
        project = project_serializer.data


    payload['message'] = "Successful"
    payload['data'] = project

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_project(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")
        title = request.data.get('title', "")
        details = request.data.get('details', "")
        target = request.data.get('target', "")


        if not title:
            errors['title'] = ['Title is required.']

        if not details:
            errors['details'] = ['Details is required.']

        if not target:
            errors['target'] = ['Target is required.']

        try:
            project = Project.objects.get(project_id=project_id)
        except:
            errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        project.title=title
        project.details=details
        project.target=target
        project.save()




        data["project_id"] = project.project_id



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_project(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")

        if not project_id:
            errors['project_id'] = ['News ID is required.']

        try:
            project = Project.objects.get(project_id=project_id)
        except:
            errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        project.is_archived = True
        project.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_project(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")

        if not project_id:
            errors['project_id'] = ['News ID is required.']

        try:
            project = Project.objects.get(project_id=project_id)
        except:
            errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        project.is_archived = False
        project.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_project(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        project_id = request.data.get('project_id', "")

        if not project_id:
            errors['project_id'] = ['News ID is required.']

        try:
            project = Project.objects.get(project_id=project_id)
        except:
            errors['project_id'] = ['Project does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        project.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_archived_projects_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_projects = Project.objects.all().filter(is_archived=True)


    if search_query:
        all_projects = all_projects.filter(
            Q(title__icontains=search_query) |
            Q(detail_name__icontains=search_query) |
            Q(target__username__icontains=search_query)
        )


    paginator = Paginator(all_projects, page_size)

    try:
        paginated_projects = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_projects = paginator.page(1)
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)

    all_projects_serializer = AllProjectsSerializer(paginated_projects, many=True)


    data['projects'] = all_projects_serializer.data
    data['pagination'] = {
        'page_number': paginated_projects.number,
        'total_pages': paginator.num_pages,
        'next': paginated_projects.next_page_number() if paginated_projects.has_next() else None,
        'previous': paginated_projects.previous_page_number() if paginated_projects.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




