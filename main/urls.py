from django.urls import path
from main.views import show_main, register, product_details, login_user, logout_user, add_to_cart, remove_from_cart, cart_view, show_xml, show_json, show_xml_by_id, show_json_by_id , checkout_view, update_quantity

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart_view/', cart_view, name='cart_view'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('update_quantity/', update_quantity, name='update_quantity'),
]