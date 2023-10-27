from django.urls import path
from main.views import show_main, register, login_user, logout, add_to_cart, remove_from_cart, cart_view

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout, name='logout'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
]