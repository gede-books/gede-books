from django.urls import path
from main.views import show_main, get_item_json

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('get-item/', get_item_json, name='get_item_json')
]
