from django.urls import path

from news.api.views import add_news, edit_news, get_all_newss_view, get_news_details_view, archive_news, delete_news, \
    unarchive_news, get_all_archived_newss_view

app_name = 'news'

urlpatterns = [
    path('add-news/', add_news, name="add_news"),
    path('edit-news/', edit_news, name="edit_news"),
    path('get-all-news/', get_all_newss_view, name="get_all_newss_view"),
    path('get-news-details/', get_news_details_view, name="get_news_details_view"),
    path('archive-news/', archive_news, name="archive_news"),
    path('delete-news/', delete_news, name="delete_news"),
    path('unarchive-news/', unarchive_news, name="unarchive_news"),
    path('get-all-archived-news/', get_all_archived_newss_view, name="get_all_archived_newss_view"),

]
