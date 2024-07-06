
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.api.serializers import AllCategorySerializer, CategoryDetailsSerializer, AllProductSerializer, \
    ProductDetailsSerializer
from shop.models import Category, Product, ProductImage, ProductVideo

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_product(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        category_id = request.data.get('category_id', "")
        name = request.data.get('name', "")
        description = request.data.get('description', "")
        stock = request.data.get('stock', "")
        price = request.data.get('price', "")

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        if not name:
            errors['name'] = ['Name is required.']

        elif check_product_name_exist(name):
            errors['name'] = ['Product name already exists in our database.']

        if not description:
            errors['description'] = ['Description is required.']

        if not stock:
            errors['stock'] = ['Stock is required.']

        if not price:
            errors['price'] = ['Price is required.']


        try:
            category = Category.objects.get(id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_product = Product.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            stock=stock,
        )

        data["product_id"] = new_product.product_id


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

def check_product_name_exist(name):
    qs = Product.objects.filter(name=name)
    if qs.exists():
        return True
    else:
        return False



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_product_images(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")

        images = request.data.get('images', [])

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            new_image = ProductImage.objects.create(
                product=product,
                image=image
            )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_product_videos(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")

        videos = request.data.get('videos', [])

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        for video in videos:
            new_video = ProductVideo.objects.create(
                product=product,
                video=video
            )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_product_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_products = Product.objects.all().filter(is_archived=False)


    if search_query:
        all_products = all_products.filter(
            Q(product_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )


    paginator = Paginator(all_products, page_size)

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    all_products_serializer = AllProductSerializer(paginated_products, many=True)


    data['products'] = all_products_serializer.data
    data['pagination'] = {
        'page_number': paginated_products.number,
        'total_pages': paginator.num_pages,
        'next': paginated_products.next_page_number() if paginated_products.has_next() else None,
        'previous': paginated_products.previous_page_number() if paginated_products.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_product_details_view(request):
    payload = {}
    data = {}
    errors = {}

    product_id = request.query_params.get('product_id', None)

    if not product_id:
        errors['product_id'] = ["Product id required"]

    try:
        product = Product.objects.get(product_id=product_id)
    except:
        errors['product_id'] = ['Product does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    product_serializer = ProductDetailsSerializer(product, many=False)
    if product_serializer:
        product = product_serializer.data


    payload['message'] = "Successful"
    payload['data'] = product

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_product(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")
        category_id = request.data.get('category_id', "")
        name = request.data.get('name', "")
        description = request.data.get('description', "")
        stock = request.data.get('stock', "")
        price = request.data.get('price', "")

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        if not name:
            errors['name'] = ['Name is required.']

        elif check_product_name_exist(name):
            errors['name'] = ['Product name already exists in our database.']

        if not description:
            errors['description'] = ['Description is required.']

        if not stock:
            errors['stock'] = ['Stock is required.']

        if not price:
            errors['price'] = ['Price is required.']


        try:
            category = Category.objects.get(id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']



        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        product.category = category
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.save()

        data["product_id"] = product.product_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_product(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        product.is_archived = True
        product.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_product(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        product.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_product(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        product.is_archived = False
        product.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_archived_products_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_products = Product.objects.all().filter(is_archived=True)


    if search_query:
        all_products = all_products.filter(
            Q(product_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(all_products, page_size)

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    all_products_serializer = AllProductSerializer(paginated_products, many=True)


    data['products'] = all_products_serializer.data
    data['pagination'] = {
        'page_number': paginated_products.number,
        'total_pages': paginator.num_pages,
        'next': paginated_products.next_page_number() if paginated_products.has_next() else None,
        'previous': paginated_products.previous_page_number() if paginated_products.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


