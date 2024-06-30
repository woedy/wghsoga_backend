import os
import random
import re
import string
from django.contrib.auth import get_user_model, authenticate




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_otp_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id





def generate_email_token():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code



def unique_profile_id_generator(instance):
    """
    This is for a profile_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    profile_id = "PRO-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(L)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(profile_id=profile_id).exists()
    if qs_exists:
        return None
    return profile_id




def unique_room_id_generator(instance):
    """
    This is for a room_id field
    :param instance:
    :return:
    """
    size = random.randint(30, 45)
    room_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(room_id=room_id).exists()
    if qs_exists:
        return None
    return room_id




def unique_project_id_generator(instance):
    """
    This is for a project_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    project_id = "PROJ-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(T)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(project_id=project_id).exists()
    if qs_exists:
        return None
    return project_id



def unique_news_id_generator(instance):
    """
    This is for a news_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    news_id = "NEWS-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(N)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(news_id=news_id).exists()
    if qs_exists:
        return None
    return news_id
def unique_event_id_generator(instance):
    """
    This is for a event_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    event_id = "EV-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(NT)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(event_id=event_id).exists()
    if qs_exists:
        return None
    return event_id


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext
