from django.urls import path
from .views import *

urlpatterns=[
    path('',index),
    path('<int:category_id>/products/',show_category_products),
    path('product/<int:product_id>',product_details),
    path('allproducts/',all_products),
    path('register/',register_user),
    path('login/',login_user),
    path('logout/',logout_user),
    path('addtocart/<int:product_id>/',add_to_cart),
    path('cart/',show_cart),
    path('remove_cart_item/<int:cart_id>/',remove_cart_item),
    path('postorder/<int:product_id>/<int:cart_id>/',post_order),
    path('myorder/',my_order),
    path('removeorder/<int:order_id>/',remove_order_item),
    path('esewaform/',EsewaView.as_view(),name='esewaform'), # name is from the reverse(from post_order function in views)
    path('esewa_verify/<int:order_id>/<int:cart_id>',esewa_verify),
    path('updateprofile/',update_profile),
    path('profile/',profile),
]