from django.urls import path
from .views import *

urlpatterns=[
    path('categories/',show_category),
    path('category/<int:category_id>/products',show_category_products),
    path('product/<int:product_id>',product_details),
    path('category/products/addproduct/',add_product),
    path('categories/addcategory/',add_category),
    path('delete_product/<int:product_id>',delete_product),
    path('delete_category/<int:category_id>',delete_category),
    path('updateproduct/<int:product_id>',update_product),
    path('updatecategory/<int:category_id>',update_category),
]