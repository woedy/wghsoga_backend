import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from wghsoga_project.utils import unique_project_id_generator, get_file_ext
User = get_user_model()


class Project(models.Model):
    project_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    target = models.CharField(max_length=500, null=True, blank=True)
    raised = models.CharField(max_length=500, null=True, blank=True)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



def pre_save_project_id_receiver(sender, instance, *args, **kwargs):
    if not instance.project_id:
        instance.project_id = unique_project_id_generator(instance)

pre_save.connect(pre_save_project_id_receiver, sender=Project)





def upload_project_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "project/images/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_project_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "project/video/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_images")
    image = models.ImageField(upload_to=upload_project_image_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_videos")
    video = models.FileField(upload_to=upload_project_video_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ProjectSupporter(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_supporters")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supporters")
    amount = models.CharField(max_length=500, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)