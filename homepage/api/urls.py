from django.urls import path

from homepage.api.views import get_home_data

app_name = 'homepage'

urlpatterns = [

    path('get-homepage-data/', get_home_data, name="get_home_data")
    ]
