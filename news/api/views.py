from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from news.api.serializers import NewsDetailsSerializer, AllNewsSerializer
from news.models import News, NewsImage, NewsVideo, NewsComment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        title = request.data.get('title', "")
        content = request.data.get('content', "")
        author_id = request.data.get('author_id', "")

        if not title:
            errors['title'] = ['Title is required.']

        if not content:
            errors['content'] = ['Content is required.']

        if not author_id:
            errors['author_id'] = ['Author ID is required.']

        try:
            author = User.objects.get(user_id=author_id)
        except:
            errors['author_id'] = ['Author Does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        new_news = News.objects.create(
            title=title,
            content=content,
            author=author,
        )


        data["news_id"] = new_news.news_id



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_news_images(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")


        images = request.data.get('images', [])

        try:
           news = News.objects.get(news_id=news_id)
        except:
           errors['news_id'] = ['News does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        for image in images:
            new_image = NewsImage.objects.create(
                news=news,
                image=image
            )


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_news_videos(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")


        videos = request.data.get('videos', [])

        try:
           news = News.objects.get(news_id=news_id)
        except:
           errors['news_id'] = ['News does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        for video in videos:
            new_video = NewsVideo.objects.create(
                news=news,
                video=video
            )


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_newss_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_newss = News.objects.all().filter(is_archived=False)


    if search_query:
        all_newss = all_newss.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__user_id__icontains=search_query)
        )


    paginator = Paginator(all_newss, page_size)

    try:
        paginated_newss = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_newss = paginator.page(1)
    except EmptyPage:
        paginated_newss = paginator.page(paginator.num_pages)

    all_newss_serializer = AllNewsSerializer(paginated_newss, many=True)


    data['newss'] = all_newss_serializer.data
    data['pagination'] = {
        'page_number': paginated_newss.number,
        'total_pages': paginator.num_pages,
        'next': paginated_newss.next_page_number() if paginated_newss.has_next() else None,
        'previous': paginated_newss.previous_page_number() if paginated_newss.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)







@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_news_details_view(request):
    payload = {}
    data = {}
    errors = {}

    news_id = request.query_params.get('news_id', None)

    if not news_id:
        errors['news_id'] = ["News id required"]

    try:
        news = News.objects.get(news_id=news_id)
    except:
        errors['news_id'] = ['News does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    news_serializer = NewsDetailsSerializer(news, many=False)
    if news_serializer:
        news = news_serializer.data


    payload['message'] = "Successful"
    payload['data'] = news

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")
        title = request.data.get('title', "")
        content = request.data.get('content', "")
        author_id = request.data.get('author_id', "")


        if not title:
            errors['title'] = ['Title is required.']

        if not content:
            errors['content'] = ['Content is required.']

        if not author_id:
            errors['author_id'] = ['Author ID is required.']

        try:
            author = User.objects.get(user_id=author_id)
        except:
            errors['author_id'] = ['Author Does not exist.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News Does not exist.']




        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        news.title=title
        news.content=content
        news.author=author
        news.save()


        data["news_id"] = news.news_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        news.is_archived = True
        news.save()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        news.is_archived = False
        news.save()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        news.delete()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_archived_newss_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_newss = News.objects.all().filter(is_archived=True)


    if search_query:
        all_newss = all_newss.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )


    paginator = Paginator(all_newss, page_size)

    try:
        paginated_newss = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_newss = paginator.page(1)
    except EmptyPage:
        paginated_newss = paginator.page(paginator.num_pages)

    all_newss_serializer = AllNewssSerializer(paginated_newss, many=True)


    data['newss'] = all_newss_serializer.data
    data['pagination'] = {
        'page_number': paginated_newss.number,
        'total_pages': paginator.num_pages,
        'next': paginated_newss.next_page_number() if paginated_newss.has_next() else None,
        'previous': paginated_newss.previous_page_number() if paginated_newss.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_news_comment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")
        comment = request.data.get('comment', "")
        user_id = request.data.get('user_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']

        if not comment:
            errors['comment'] = ['Comment is required.']

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User Does not exist.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News Does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        comment = NewsComment.objects.create(
            news=news,
            comment=comment,
            user=user
        )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_news_likes(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")
        user_id = request.data.get('user_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User Does not exist.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News Does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        news.likes.add(user)
        news.save()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def share_news(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        news_id = request.data.get('news_id', "")
        user_id = request.data.get('user_id', "")

        if not news_id:
            errors['news_id'] = ['News ID is required.']


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User Does not exist.']

        try:
            news = News.objects.get(news_id=news_id)
        except:
            errors['news_id'] = ['News Does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        news.shares.add(user)
        news.save()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
