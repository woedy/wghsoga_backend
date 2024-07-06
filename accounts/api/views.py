import re

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import UserRegistrationSerializer, PasswordResetSerializer, ListAllUsersSerializer, \
    UserDetailsSerializer
from activities.models import AllActivity
from communications.models import PrivateChatRoom
from user_profile.models import UserProfile, UserPhoto, UserInterest
from wghsoga_project.utils import generate_email_token, generate_random_otp_code

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def validate_email(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email or User already exists in our database.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()

        first_name = request.data.get('first_name', "")
        middle_name = request.data.get('middle_name', "")
        last_name = request.data.get('last_name', "")

        username = request.data.get('username', "")
        country = request.data.get('country', "")
        phone = request.data.get('phone', "")

        year_group = request.data.get('year_group', "")

        password = request.data.get('password', "")
        password2 = request.data.get('password2', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not year_group:
            errors['year_group'] = ['Year group is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not password:
            errors['password'] = ['Password is required.']

        if not password2:
            errors['password2'] = ['Password2 is required.']

        if password != password2:
            errors['password'] = ['Passwords dont match.']

        if not is_valid_password(password):
            errors['password'] = [
                'Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data["user_id"] = user.user_id
            data["email"] = user.email
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name

            room = PrivateChatRoom.objects.create(
                user=user
            )

        user.username = username
        user.year_group = year_group
        user.country = country
        user.phone = phone
        user.save()

        user_profile = UserProfile.objects.create(
            user=user,
            room=room,
        )



        ## Generate token using the custom serializer
        #serializer = CustomTokenObtainPairSerializer()
        #_token = serializer.get_token(user)
#
        #token = {
        #    'refresh': str(_token),
        #    'access': str(_token.access_token),
        #}

        token = Token.objects.get(user=user)

        data['token'] = token.key

        email_token = generate_email_token()

        user = User.objects.get(email=email)
        user.email_token = email_token
        user.save()

        context = {
            'email_token': email_token,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

        txt_ = get_template("registration/emails/verify.html").render(context)
        html_ = get_template("registration/emails/verify.txt").render(context)

        subject = 'EMAIL CONFIRMATION CODE'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            txt_,
            from_email,
            recipient_list,
            html_message=html_,
            fail_silently=False,
        )

        #
        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Registration",
            body=user.email + " Just created an account."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




def check_email_exist(email):
    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False
def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[-!@#\$%^&*_()-+=/.,<>?"~`£{}|:;]', password):
        return False

    return True






@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_deleted = True
        user.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def verify_user_email(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    token_errors = []

    email = request.data.get('email', '').lower()
    email_token = request.data.get('email_token', '')

    if not email:
        email_errors.append('Email is required.')

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')

    if email_errors:
        errors['email'] = email_errors

    if not email_token:
        token_errors.append('Token is required.')

    user = None
    if qs.exists():
        user = qs.first()
        if email_token != user.email_token:
            token_errors.append('Invalid Token.')

    if token_errors:
        errors['email_token'] = token_errors

    if email_errors or token_errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    user.is_active = True
    user.email_verified = True
    user.save()

    data["user_id"] = user.user_id
    data["email"] = user.email

    payload['message'] = "Successful"
    payload['data'] = data

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Verify Email",
        body=user.email + " just verified their email",
    )
    new_activity.save()

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def resend_email_verification(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []

    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_email_token()
    user.email_token = otp_code
    user.save()

    context = {
        'email_token': otp_code,
        'email': user.email,
        'first_name': user.first_name
    }

    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
    # # Execute the Celery chain asynchronously
    # email_chain.apply_async()

    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )

    #data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Email verification sent",
        body="Email verification sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = {}
        data = {}
        errors = {}

        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')
        fcm_token = request.data.get('fcm_token', '')

        if not email:
            errors['email'] = ['Email is required.']

        if not password:
            errors['password'] = ['Password is required.']

        if not fcm_token:
            errors['fcm_token'] = ['FCM device token is required.']

        try:
            qs = User.objects.filter(email=email)
        except User.DoesNotExist:
            errors['email'] = ['User does not exist.']

        if qs.exists():
            not_active = qs.filter(email_verified=False)
            if not_active:
                errors['email'] = ["Please check your email to confirm your account or resend confirmation email."]

        if not check_password(email, password):
            errors['password'] = ['Invalid Credentials']

        user = authenticate(email=email, password=password)

        if not user:
            errors['email'] = ['Invalid Credentials']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        ## Generate token using the custom serializer
        #serializer = CustomTokenObtainPairSerializer()
        #_token = serializer.get_token(user)
#
        #token = {
        #    'refresh': str(_token),
        #    'access': str(_token.access_token),
        #}

        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)



        user.fcm_token = fcm_token
        user.save()

        data["user_id"] = user.user_id
        data["email"] = user.email
        data["first_name"] = user.first_name
        data["middle_name"] = user.middle_name
        data["last_name"] = user.last_name
        data["year_group"] = user.year_group
        data["country"] = user.country

        data['token'] = token.key

        payload['message'] = "Successful"
        payload['data'] = data

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Login",
            body=user.email + " Just logged in."
        )
        new_activity.save()

        return Response(payload, status=status.HTTP_200_OK)


def check_password(email, password):
    try:
        user = User.objects.get(email=email)
        return user.check_password(password)
    except User.DoesNotExist:
        return False



class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer



    def post(self, request, *args, **kwargs):
        payload = {}
        data = {}
        errors = {}
        email_errors = []

        email = request.data.get('email', '').lower()

        if not email:
            email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        qs = User.objects.filter(email=email)
        if not qs.exists():
            email_errors.append('Email does not exist.')
            if email_errors:
                errors['email'] = email_errors
                payload['message'] = "Error"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_404_NOT_FOUND)


        user = User.objects.filter(email=email).first()
        otp_code = generate_random_otp_code()
        user.otp_code = otp_code
        user.save()

        context = {
            'otp_code': otp_code,
            'email': user.email,
            'first_name': user.first_name
        }

        txt_ = get_template("registration/emails/send_otp.txt").render(context)
        html_ = get_template("registration/emails/send_otp.html").render(context)

        subject = 'OTP CODE'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        #  )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            txt_,
            from_email,
            recipient_list,
            html_message=html_,
            fail_silently=False,
        )

        data["otp_code"] = otp_code
        data["email"] = user.email
        data["user_id"] = user.user_id

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Reset Password",
            body="OTP sent to " + user.email,
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

        return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def confirm_otp_password_view(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    otp_errors = []

    email = request.data.get('email', '').lower()
    otp_code = request.data.get('otp_code', '')

    if not email:
        email_errors.append('Email is required.')

    if not otp_code:
        otp_errors.append('OTP code is required.')

    user = User.objects.filter(email=email).first()

    if user is None:
        email_errors.append('Email does not exist.')

    client_otp = user.otp_code if user else ''

    if client_otp != otp_code:
        otp_errors.append('Invalid Code.')

    if email_errors or otp_errors:
        errors['email'] = email_errors
        errors['otp_code'] = otp_errors
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    data['email'] = user.email if user else ''
    data['user_id'] = user.user_id if user else ''

    payload['message'] = "Successful"
    payload['data'] = data
    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def resend_password_otp(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []

    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_random_otp_code()
    user.otp_code = otp_code
    user.save()

    context = {
        'otp_code': otp_code,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    txt_ = get_template("registration/emails/send_otp.txt").render(context)
    html_ = get_template("registration/emails/send_otp.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
    # # Execute the Celery chain asynchronously
    # email_chain.apply_async()

    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )

    #data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Password OTP sent",
        body="Password OTP sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def new_password_reset_view(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []
    password_errors = []

    email = request.data.get('email', '0').lower()
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')

    if not email:
        email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exists.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    if not new_password:
        password_errors.append('Password required.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    if new_password != new_password2:
        password_errors.append('Password don\'t match.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    user.set_password(new_password)
    user.save()

    data['email'] = user.email
    data['user_id'] = user.user_id

    payload['message'] = "Successful, Password reset successfully."
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def update_user_info_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        user_id = request.data.get('user_id', "")
        photos = request.data.get('photos', [])
        bio = request.data.get('bio', "")
        interests = request.data.get('interests', [])
        profession = request.data.get('profession', "")
        job_title = request.data.get('job_title', "")
        place_of_work = request.data.get('place_of_work', "")
        city = request.data.get('city', "")
        house = request.data.get('house', "")

        website = request.data.get('website', "")
        linked_in = request.data.get('linked_in', "")
        instagram = request.data.get('instagram', "")
        facebook = request.data.get('facebook', "")
        twitter = request.data.get('twitter', "")


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            profile = UserProfile.objects.get(user=user)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        if user:
            user.about_me = bio
            user.save()

        if profile:
            profile.profession = profession
            profile.job_title = job_title
            profile.place_of_work = place_of_work
            profile.city = city

            profile.house = house

            profile.website = website
            profile.linked_in = linked_in
            profile.instagram = instagram
            profile.facebook = facebook
            profile.twitter = twitter

            profile.save()


        for photo in photos:
            new_photo = UserPhoto.objects.create(
                user=user,
                photo=photo
            )

        for interest in interests:
            new_interest = UserInterest.objects.create(
                user=user,
                interest=interest
            )

        user_photos = UserPhoto.objects.filter(
            user=user
        ).first()

        user.photo = user_photos.photo
        user.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def edit_account(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        user_id = request.data.get('user_id', "")
        #email = request.data.get('email', "").lower()
        first_name = request.data.get('first_name', "")
        middle_name = request.data.get('middle_name', "")
        last_name = request.data.get('last_name', "")
        country = request.data.get('country', "")
        username = request.data.get('username', "")
        phone = request.FILES.get('phone')

        #if not email:
        #    errors['email'] = ['User Email is required.']
        #elif not is_valid_email(email):
        #    errors['email'] = ['Valid email required.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.username = username
            user.country = country
            user.phone = phone
            #user.email = email
            user.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_users_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    filter_year_group = request.query_params.get('filter_year_group', "")
    page_size = 10

    users = User.objects.filter(is_archived=False)

    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(marital_status__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(language__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )

    if filter_year_group:
        users = users.filter(
            Q(year_group__icontains=filter_year_group),
        )

    paginator = Paginator(users, page_size)

    try:
        paginated_users = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    users_serializer = ListAllUsersSerializer(paginated_users, many=True)

    data['users'] = users_serializer.data
    data['pagination'] = {
        'page_number': paginated_users.number,
        'total_pages': paginator.num_pages,
        'next': paginated_users.next_page_number() if paginated_users.has_next() else None,
        'previous': paginated_users.previous_page_number() if paginated_users.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_archived_users_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    filter_year_group = request.query_params.get('filter_year_group', "")
    page_size = 10

    users = User.objects.filter(is_archived=True)

    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(marital_status__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(language__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )

    if filter_year_group:
        users = users.filter(
            Q(year_group__icontains=filter_year_group),
        )

    paginator = Paginator(users, page_size)

    try:
        paginated_users = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    users_serializer = ListAllUsersSerializer(paginated_users, many=True)

    data['users'] = users_serializer.data
    data['pagination'] = {
        'page_number': paginated_users.number,
        'total_pages': paginator.num_pages,
        'next': paginated_users.next_page_number() if paginated_users.has_next() else None,
        'previous': paginated_users.previous_page_number() if paginated_users.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_details_view(request):
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


    user_detail_serializer = UserDetailsSerializer(user, many=False)
    if user_detail_serializer:
        user_detail = user_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = user_detail

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def archive_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account Archived",
            body=user.email + " account archived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def unarchive_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = False
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account unarchived",
            body=user.email + " account unarchived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def delete_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

