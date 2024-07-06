
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.api.serializers import AllCategorySerializer, CategoryDetailsSerializer
from shop.models import Category

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_category(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        name = request.data.get('name', "")
        description = request.data.get('description', "")

        if not name:
            errors['name'] = ['Name is required.']

        elif check_category_name_exist(name):
            errors['name'] = ['Category name already exists in our database.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_category = Category.objects.create(
            name=name,
            description=description,
        )

        data["category_id"] = new_category.id


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

def check_category_name_exist(name):
    qs = Category.objects.filter(name=name)
    if qs.exists():
        return True
    else:
        return False




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_category_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_categories = Category.objects.all()


    if search_query:
        all_categories = all_categories.filter(
            Q(category_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description_number__icontains=search_query)
        )


    paginator = Paginator(all_categories, page_size)

    try:
        paginated_categories = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_categories = paginator.page(1)
    except EmptyPage:
        paginated_categories = paginator.page(paginator.num_pages)

    all_categories_serializer = AllCategorySerializer(paginated_categories, many=True)


    data['categories'] = all_categories_serializer.data
    data['pagination'] = {
        'page_number': paginated_categories.number,
        'total_pages': paginator.num_pages,
        'next': paginated_categories.next_page_number() if paginated_categories.has_next() else None,
        'previous': paginated_categories.previous_page_number() if paginated_categories.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_category(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        category_id = request.data.get('category_id', "")

        name = request.data.get('name', "")
        description = request.data.get('description', "")



        if not name:
            errors['name'] = ['Name is required.']

        elif check_category_name_exist(name):
            errors['name'] = ['Category name already exists in our database.']


        try:
            category = Category.objects.get(id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        category.name = name
        category.description = description
        category.save()

        data["category_id"] = category.id


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_category(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        category_id = request.data.get('category_id', "")

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        try:
            category = Category.objects.get(category_id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        category.is_archived = True
        category.save()



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_category(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        category_id = request.data.get('category_id', "")

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        try:
            category = Category.objects.get(id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        category.delete()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


