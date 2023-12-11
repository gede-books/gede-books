from django.urls import path
<<<<<<< HEAD
from main.views import show_main, show_guest, register, product_details, login_user, logout_user, add_to_cart, remove_from_cart, cart_view, show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import get_item_json, checkout_cart, checkout_view, update_quantity 
=======
from main.views import *
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675

app_name = 'main'

urlpatterns = [
<<<<<<< HEAD
    path('main/', show_main, name='show_main'),
    path('', show_guest, name='show_guest'),
=======
    path('', show_main, name='show_main'),
    path('guest/', show_guest, name='show_guest'),
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675
    path('register/', register, name='register'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
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
    path('get-item/', get_item_json, name='get_item_json'),
<<<<<<< HEAD
    path('checkout_cart/', checkout_cart, name='checkout_cart'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('update_quantity/', update_quantity, name='update_quantity'),
]
=======
    path('search/<str:judul>', show_search, name='show_search')
>>>>>>> cb2366c7a62a2fb7e99ca49eabc216a9ed650675
