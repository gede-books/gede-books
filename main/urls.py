from django.urls import path
from main.views import show_main, show_guest, register, product_details, login_user, logout_user, add_to_cart, remove_from_cart, cart_view, show_xml, show_json, show_xml_by_id, show_json_by_id
<<<<<<< HEAD
from main.views import get_item_json, checkout_cart, checkout_view, update_quantity, add_to_wishlist, remove_from_wishlist, wishlist_view
=======
from main.views import get_item_json, checkout_cart, checkout_view, update_quantity, add_to_wishlist, wishlist_view
>>>>>>> 9a63bcb9bbda8b6e95590ea795f502f2b1331832

app_name = 'main'

urlpatterns = [
    path('main/', show_main, name='show_main'),
    path('', show_guest, name='show_guest'),
    path('register/', register, name='register'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('get-item/', get_item_json, name='get_item_json'),
    path('checkout_cart/', checkout_cart, name='checkout_cart'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
<<<<<<< HEAD
    path('remove_from_wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
=======
>>>>>>> 9a63bcb9bbda8b6e95590ea795f502f2b1331832
    path('wishlist/', wishlist_view, name='wishlist_view'),
]