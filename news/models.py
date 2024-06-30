import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from wghsoga_project.utils import unique_project_id_generator, get_file_ext, unique_news_id_generator

User = get_user_model()


class News(models.Model):
    news_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=5000, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    likes = models.ManyToManyField(User, related_name='news_likes')
    shares = models.ManyToManyField(User, related_name='news_shares')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news_author")


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



def pre_save_news_id_receiver(sender, instance, *args, **kwargs):
    if not instance.news_id:
        instance.news_id = unique_news_id_generator(instance)

pre_save.connect(pre_save_news_id_receiver, sender=News)





def upload_news_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "news/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_news_video_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "news/videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_images")
    image = models.ImageField(upload_to=upload_news_image_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NewsVideo(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_videos")
    video = models.FileField(upload_to=upload_news_video_path, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)