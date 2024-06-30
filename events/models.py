import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from wghsoga_project.utils import unique_event_id_generator, get_file_ext

User = get_user_model()

class Event(models.Model):
    event_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    theme = models.CharField(max_length=1000, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)

    attendees = models.ManyToManyField(User, related_name='event_attendees')

    event_date = models.DateField(null=True, blank=True)
    event_time = models.TimeField(null=True, blank=True)

    venue = models.CharField(max_length=1000, null=True, blank=True)
    organised_by = models.CharField(max_length=1000, null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



def pre_save_event_id_receiver(sender, instance, *args, **kwargs):
    if not instance.event_id:
        instance.event_id = unique_event_id_generator(instance)

pre_save.connect(pre_save_event_id_receiver, sender=Event)







def upload_event_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "news/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_event_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "event/videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_images")
    image = models.ImageField(upload_to=upload_event_image_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EventVideo(models.Model):
    news = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_videos")
    video = models.FileField(upload_to=upload_event_video_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

