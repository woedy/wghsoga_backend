from django.contrib import admin

from user_profile.models import UserPhoto, UserProfile, UserInterest

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPhoto)
admin.site.register(UserInterest)
