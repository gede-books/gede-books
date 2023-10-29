from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('guest/', show_guest, name='show_guest'),
    path('register/', register, name='register'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart_view/', cart_view, name='cart_view'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout_cart/', checkout_cart, name='checkout_cart'),
    path('purchased_books/', purchased_books, name='purchased_books'),
    path('purchased_books_ajax/', purchased_books_ajax, name='purchased_books_ajax'),
    path('tinggalkan_review/<int:id>', tinggalkan_review, name='tinggalkan_review'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('get-item/', get_item_json, name='get_item_json'),
    path('search/<str:judul>', show_search, name='show_search')
]
