
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
from shop.api.serializers import AllOrdersSerializer, OrderDetailsSerializer
from shop.models import Order, OrderItem, Product, ShippingAddress


User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_orders = Order.objects.all().filter(is_archived=False).order_by('-created_at')

    if search_query:
        all_orders = all_orders.filter(
            Q(customer__first_name__icontains=search_query) 
        )


    paginator = Paginator(all_orders, page_size)

    try:
        paginated_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    all_orders_serializer = AllOrdersSerializer(paginated_orders, many=True)

    data['orders'] = all_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_orders.next_page_number() if paginated_orders.has_next() else None,
        'previous': paginated_orders.previous_page_number() if paginated_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def set_order_delivered(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        status = 'Delivered'
        order.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def place_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        product_id = request.data.get('product_id', "")
        quantity = request.data.get('quantity', 0)
        user_id = request.data.get('user_id', "")

        address = request.data.get('address', "")
        country = request.data.get('country', "")


        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not address:
            errors['address'] = ['Shipping Address is required.']

        if not country:
            errors['country'] = ['Country is required.']

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_order = Order.objects.create(
            customer=user         
        )

        new_order_item = OrderItem.objects.create(
            order=new_order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        new_shipping_address = ShippingAddress.create(
            order=new_order,
            address=address,
            country=country
        )

        data["order_id"] = new_order.order_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_user_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', '')

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10


    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']



    all_orders = Order.objects.all().filter(is_archived=False, customer=user).order_by('-created_at')


    paginator = Paginator(all_orders, page_size)

    try:
        paginated_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    all_orders_serializer = AllOrdersSerializer(paginated_orders, many=True)

    data['orders'] = all_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_orders.next_page_number() if paginated_orders.has_next() else None,
        'previous': paginated_orders.previous_page_number() if paginated_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_order_details_view(request):
    payload = {}
    data = {}
    errors = {}

    order_id = request.query_params.get('order_id', None)

    if not order_id:
        errors['order_id'] = ["Order id required"]

    try:
        order = Order.objects.get(order_id=order_id)
    except:
        errors['order_id'] = ['Order ID does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    order_serializer = OrderDetailsSerializer(order, many=False)
    if order_serializer:
        order = order_serializer.data

    payload['message'] = "Successful"
    payload['data'] = order

    return Response(payload, status=status.HTTP_200_OK)
