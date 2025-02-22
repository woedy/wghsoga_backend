
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from dues.api.serializers import AllDuesEntrysSerializer, DuesEntryDetailsSerializer
from dues.models import BankAccount, DuesEntry, DuesPayPeriod




User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def pay_dues(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        amount = request.data.get('amount', 0)
        reference = request.data.get('reference', "")



        if not user_id:
            errors['user_id'] = ['User ID is required.']


        if not amount:
            errors['amount'] = ['Amount is required.']

        
        if not reference:
            errors['reference'] = ['Reference is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']





        try:
            account = BankAccount.objects.get(year_group=user.year_group)
        except:
            errors['user_id'] = ['Bank Account does not exist.']


        pay_period = DuesPayPeriod.objects.all().order_by('-created_at').first()


        try:
            entry = DuesEntry.objects.get(user=user, pay_period=pay_period)
            errors['dues_id'] = ['Dues entry for the pay period already exist.']
        except:
            pass

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_dues_entry = DuesEntry.objects.create(
            user=user,
            pay_period=pay_period,
            amount=amount,
            reference=reference,
    

        )
        data['dues_id'] = new_dues_entry.dues_id

        account.deposit(Decimal(amount), 'Paid Dues')


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_get_all_dues_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    user_id = request.query_params.get('user_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_dues_entrys = DuesEntry.objects.all().filter(is_archived=False)


    if search_query:
        all_dues_entrys = all_dues_entrys.filter(
            Q(user__user_id__icontains=search_query) |
            Q(pay_period__start_date__icontains=search_query)
        )


    # Apply filters dynamically
    if user_id:
        all_dues_entrys = all_dues_entrys.filter(user__user_id__icontains=user_id)

    paginator = Paginator(all_dues_entrys, page_size)

    try:
        paginated_dues_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_dues_entrys = paginator.page(1)
    except EmptyPage:
        paginated_dues_entrys = paginator.page(paginator.num_pages)

    all_dues_entrys_serializer = AllDuesEntrysSerializer(paginated_dues_entrys, many=True)


    data['dues_entries'] = all_dues_entrys_serializer.data
    data['pagination'] = {
        'page_number': paginated_dues_entrys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_dues_entrys.next_page_number() if paginated_dues_entrys.has_next() else None,
        'previous': paginated_dues_entrys.previous_page_number() if paginated_dues_entrys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_dues_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    user_id = request.query_params.get('user_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_dues_entrys = DuesEntry.objects.all().filter(is_archived=False)


    if search_query:
        all_dues_entrys = all_dues_entrys.filter(
            Q(user__user_id__icontains=search_query) |
            Q(pay_period__start_date__icontains=search_query)
        )


    # Apply filters dynamically
    if user_id:
        all_dues_entrys = all_dues_entrys.filter(user__user_id__icontains=user_id)

    paginator = Paginator(all_dues_entrys, page_size)

    try:
        paginated_dues_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_dues_entrys = paginator.page(1)
    except EmptyPage:
        paginated_dues_entrys = paginator.page(paginator.num_pages)

    all_dues_entrys_serializer = AllDuesEntrysSerializer(paginated_dues_entrys, many=True)


    data['dues_entries'] = all_dues_entrys_serializer.data
    data['pagination'] = {
        'page_number': paginated_dues_entrys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_dues_entrys.next_page_number() if paginated_dues_entrys.has_next() else None,
        'previous': paginated_dues_entrys.previous_page_number() if paginated_dues_entrys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_dues_entry_details_view(request):
    payload = {}
    data = {}
    errors = {}

    dues_id = request.query_params.get('dues_id', None)

    if not dues_id:
        errors['dues_id'] = ["Dues ID required"]

    try:
        dues_entry = DuesEntry.objects.get(dues_id=dues_id)
    except:
        errors['dues_id'] = ['Dues Entry does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    dues_entry_serializer = DuesEntryDetailsSerializer(dues_entry, many=False)
    if dues_entry_serializer:
        dues_entry = dues_entry_serializer.data


    payload['message'] = "Successful"
    payload['data'] = dues_entry

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_dues_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        dues_id = request.data.get('dues_id', "")

        user_id = request.data.get('user_id', "")
        pay_period_id = request.data.get('pay_period_id', "")
        amount = request.data.get('amount', 0)
        reference = request.data.get('reference', "")





        if not user_id:
            errors['dues_id'] = ['Dues ID is required.']


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not pay_period_id:
            errors['pay_period_id'] = ['Pay Period ID is required.']

        if not amount:
            errors['amount'] = ['Amount is required.']

        
        if not reference:
            errors['reference'] = ['Reference is required.']

        try:
            dues_entry = DuesEntry.objects.get(dues_id=dues_id)
        except:
            errors['dues_id'] = ['Dues entry does not exist.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            pay_period = DuesPayPeriod.objects.get(id=pay_period_id)
        except:
            errors['pay_period_id'] = ['Pay Period does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        dues_entry.user = user
        dues_entry.pay_period = pay_period
        dues_entry.amount = amount
        dues_entry.reference = reference

        dues_entry.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_dues_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        dues_id = request.data.get('dues_id', "")

        if not dues_id:
            errors['dues_id'] = ['ID is required.']

        try:
            dues_entry = DuesEntry.objects.get(dues_id=dues_id)
        except:
            errors['dues_id'] = ['Dues Entry does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        dues_entry.is_archived = True
        dues_entry.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_dues_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        dues_id = request.data.get('dues_id', "")

        if not dues_id:
            errors['dues_id'] = ['ID is required.']

        try:
            dues_entry = DuesEntry.objects.get(dues_id=dues_id)
        except:
            errors['dues_id'] = ['Dues Entry does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        dues_entry.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_dues_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        dues_id = request.data.get('dues_id', "")

        if not dues_id:
            errors['dues_id'] = ['ID is required.']

        try:
            dues_entry = DuesEntry.objects.get(dues_id=dues_id)
        except:
            errors['dues_id'] = ['Dues Entry does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        dues_entry.is_archived = False
        dues_entry.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_all_archived_dues_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payroll_entrys = DuesPayPeriod.objects.all().filter(is_archived=True)


    if search_query:
        all_payroll_entrys = all_payroll_entrys.filter(
            Q(user__user_id__icontains=search_query) |
            Q(staff_pay_period__start_date__icontains=search_query)
        )


    paginator = Paginator(all_payroll_entrys, page_size)

    try:
        paginated_payroll_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_payroll_entrys = paginator.page(1)
    except EmptyPage:
        paginated_payroll_entrys = paginator.page(paginator.num_pages)

    all_payroll_entrys_serializer = AllDuesEntrysSerializer(paginated_payroll_entrys, many=True)


    data['payroll_entries'] = all_payroll_entrys_serializer.data
    data['pagination'] = {
        'page_number': paginated_payroll_entrys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_payroll_entrys.next_page_number() if paginated_payroll_entrys.has_next() else None,
        'previous': paginated_payroll_entrys.previous_page_number() if paginated_payroll_entrys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
