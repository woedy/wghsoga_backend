import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

from communications.models import PrivateChatRoom
from wghsoga_project.utils import unique_profile_id_generator, get_file_ext

User = get_user_model()



def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "user_photos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_id = models.CharField(max_length=200, null=True, blank=True)

    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="guards_user_room")

    profession = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    place_of_work = models.CharField(max_length=255, blank=True, null=True,)
    city = models.CharField(max_length=255, blank=True, null=True)

    house = models.CharField(max_length=255, blank=True, null=True)

    website = models.CharField(max_length=255, blank=True, null=True)
    linked_in = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)


    profile_complete = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)


    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def pre_save_profile_id_receiver(sender, instance, *args, **kwargs):
    if not instance.profile_id:
        instance.profile_id = unique_profile_id_generator(instance)

pre_save.connect(pre_save_profile_id_receiver, sender=UserProfile)


class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
    photo = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_interests')
    interest = models.CharField(max_length=255, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

