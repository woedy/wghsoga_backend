from django.urls import path

from projects.api.views import add_project, edit_project, get_project_details_view, get_all_projects_view, \
    archive_project, delete_project, unarchive_project, get_all_archived_projects_view

app_name = 'projects'

urlpatterns = [
    path('add-project/', add_project, name="add_project"),
    path('edit-project/', edit_project, name="edit_project"),
    path('get-all-projects/', get_all_projects_view, name="get_all_projects_view"),
    path('get-project-details/', get_project_details_view, name="get_project_details_view"),
    path('archive-project/', archive_project, name="archive_project"),
    path('delete-project/', delete_project, name="delete_project"),
    path('unarchive-project/', unarchive_project, name="unarchive_project"),
    path('get-all-archived-projects/', get_all_archived_projects_view, name="get_all_archived_projects_view"),

]
