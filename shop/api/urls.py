from django.urls import path


from shop.api.views.category_views import add_category, edit_category, delete_category, get_all_category_view
from shop.api.views.product_views import add_product, edit_product, get_all_product_view, get_product_details_view, \
    archive_product, unarchive_product, get_all_archived_products_view, delete_product, add_product_images, \
    add_product_videos

app_name = 'shop'

urlpatterns = [

    ########## Categories ####
    path('add-category/', add_category, name="add_category"),
    path('edit-category/', edit_category, name="edit_category"),
    path('delete-category/', delete_category, name="delete_category"),
    path('get-all-categories/', get_all_category_view, name="get_all_category_view"),

    ########## Products ####
    path('add-product/', add_product, name="add_product"),
    path('add-product-images/', add_product_images, name="add_product_images"),
    path('add-product-videos/', add_product_videos, name="add_product_videos"),
    path('edit-product/', edit_product, name="edit_product"),
    path('get-all-products/', get_all_product_view, name="get_all_product_view"),
    path('get-product-details/', get_product_details_view, name="get_product_details_view"),
    path('archive-product/', archive_product, name="archive_product"),
    path('unarchive-product/', unarchive_product, name="unarchive_product"),
    path('get-all-archived-products/', get_all_archived_products_view, name="get_all_archived_products_view"),
    path('delete-product/', delete_product, name="delete_product"),

]
