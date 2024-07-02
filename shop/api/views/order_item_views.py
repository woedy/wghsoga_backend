
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.api.serializers import AllOrderSerializer, OrderDetailsSerializer, AllOrderItemsSerializer, \
    OrderItemDetailsSerializer
from shop.models import Order, OrderItem, Product

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def create_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")
        product_id = request.data.get('product_id', "")
        quantity = request.data.get('quantity', "")



        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']



        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity

        )

        data["order_item_id"] = new_order_item.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_order_items_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_order_items = OrderItem.objects.all()


    if search_query:
        all_order_items = all_order_items.filter(
            Q(id__icontains=search_query)
        )


    paginator = Paginator(all_order_items, page_size)

    try:
        paginated_order_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_order_items = paginator.page(1)
    except EmptyPage:
        paginated_order_items = paginator.page(paginator.num_pages)

    all_order_items_serializer = AllOrderItemsSerializer(paginated_order_items, many=True)


    data['order_items'] = all_order_items_serializer.data
    data['pagination'] = {
        'page_number': paginated_order_items.number,
        'total_pages': paginator.num_pages,
        'next': paginated_order_items.next_page_number() if paginated_order_items.has_next() else None,
        'previous': paginated_order_items.previous_page_number() if paginated_order_items.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_order_item_details_view(request):
    payload = {}
    data = {}
    errors = {}

    order_item_id = request.query_params.get('order_item_id', None)

    if not order_item_id:
        errors['order_item_id'] = ["Order_Item id required"]

    try:
        order_item = OrderItem.objects.get(id=order_item_id)
    except:
        errors['order_item_id'] = ['Order_Item does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    order_item_serializer = OrderItemDetailsSerializer(order_item, many=False)
    if order_item_serializer:
        order_item = order_item_serializer.data


    payload['message'] = "Successful"
    payload['data'] = order_item

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def update_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id', "")
        product_id = request.data.get('product_id', "")
        quantity = request.data.get('quantity', "")


        if not order_item_id:
            errors['order_item_id'] = ['Order_Item ID is required.']

        if not product_id:
            errors['product_id'] = ['Product ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']


        try:
            order_item = OrderItem.objects.get(order_item_id=order_item_id)
        except:
            errors['order_item_id'] = ['Order Item does not exist.']


        try:
            product = Product.objects.get(product_id=product_id)
        except:
            errors['product_id'] = ['Product does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.product = product
        order_item.quantity = quantity
        order_item.save()

        data["order_item_id"] = order_item.order_item_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id', "")

        if not order_item_id:
            errors['order_item_id'] = ['Order_Item ID is required.']

        try:
            order_item = OrderItem.objects.get(id=order_item_id)
        except:
            errors['order_item_id'] = ['Order Item does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


