from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.core import serializers

# Create your views here.


def show_main(request):
    context = {
        'title': 'Anoooooomgh',
        'language': 'Zimbabwe',
        'firstName': 'Rakha',
        'lastName': 'Abid'
    }

    return render(request, "main.html", context)


def get_item_json(request):
    product_item = Product.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))
