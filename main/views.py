from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse

from main.models import Product, Order, OrderItem
from book.models import Book
from .forms import SearchForm

import datetime
import csv

@csrf_exempt
@login_required(login_url='/login')
def show_main(request):
    search_form = SearchForm(request.POST or None)

    # Ambil semua buku
    books = Book.objects.all()

    # Buat objek Product untuk setiap buku
    products = []
    for book in books:
        product = Product(
            bookCode=book.bookCode,
            title=book.title,
            language=book.language,
            firstName=book.firstName,
            lastName=book.lastName,
            year=book.year,
            subjects=book.subjects,
            category=book.category,
            stock=25,
            price=75000,
        )
        product.save()
        products.append(product)

    # Ambil parameter query dari URL atau dari POST jika ada
    search_query = request.GET.get('query') or request.POST.get('query', '')

    if search_query:
        search_query_lower = search_query.lower()
        products = [product for product in products if search_query_lower in product.title.lower()]

    # Jika ada parameter kategori, filter produk berdasarkan kategori tersebut
    selected_category = request.GET.get('category')
    if selected_category:
        products = [product for product in products if selected_category in product.category]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Buat respons untuk AJAX
        titles = [product.title for product in products]
        return JsonResponse({'titles': titles})

    # Ambil parameter sorting dari URL
    sort_by = request.GET.get('sort_by')

    # Urutkan produk berdasarkan judul buku
    if sort_by == 'az':
        products = sorted(products, key=lambda x: x.title)
    elif sort_by == 'za':
        products = sorted(products, key=lambda x: x.title, reverse=True)

    # Baca file CSV dan buat kamus untuk URL gambar
    image_map = {}
    with open('main/bookImages.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                image_map[int(row['bookCode'])] = row['image']
            except KeyError as e:
                print(f"KeyError: {e}. Row: {row}")

    # Tambahkan URL gambar ke setiap produk jika ada di kamus
    for product in products:
        if product.bookCode in image_map:
            product.image_url = image_map[product.bookCode]
        else:
            product.image_url = None

    last_login = request.COOKIES.get('last_login', 'Not available')

    # Tambahkan produk ke konteks
    context = {
        'name': request.user.username,
        'last_login': last_login,
        'products': products,
        'search_form': search_form,
        'selected_category': selected_category
    }

    return render(request, "main.html", context)

def show_guest(request):
    search_form = SearchForm(request.GET or None)

    # Ambil semua buku
    books = Book.objects.all()

    # Buat objek Product untuk setiap buku
    products = []
    for book in books:
        product = Product(
            bookCode=book.bookCode,
            title=book.title,
            language=book.language,
            firstName=book.firstName,
            lastName=book.lastName,
            year=book.year,
            subjects=book.subjects,
            category=book.category,
            stock=25,
            price=75000,
        )
        product.save()
        products.append(product)

    # Jika ada parameter judul, filter produk berdasarkan judul tersebut
    search_query = request.GET.get('query', '')
    if search_query:
        search_query_lower = search_query.lower()
        products = [product for product in products if search_query_lower in product.title.lower()]

    # Jika ada parameter kategori, filter produk berdasarkan kategori tersebut
    selected_category = request.GET.get('category')
    if selected_category:
        products = [product for product in products if selected_category in product.category]

    # Ambil parameter sorting dari URL
    sort_by = request.GET.get('sort_by')

    # Urutkan produk berdasarkan judul buku
    if sort_by == 'az':
        products = sorted(products, key=lambda x: x.title)
    elif sort_by == 'za':
        products = sorted(products, key=lambda x: x.title, reverse=True)

    # Baca file CSV dan buat kamus untuk URL gambar
    image_map = {}
    with open('main/bookImages.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                image_map[int(row['bookCode'])] = row['image']
            except KeyError as e:
                print(f"KeyError: {e}. Row: {row}")

    # Tambahkan URL gambar ke setiap produk jika ada di kamus
    for product in products:
        if product.bookCode in image_map:
            product.image_url = image_map[product.bookCode]
        else:
            product.image_url = None

    # Tambahkan produk ke konteks
    context = {
        'products': products,
        'search_form': search_form,
        'selected_category': selected_category
    }

    return render(request, "guest.html", context)

def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Load the image map again
    image_map = {}
    with open('main/bookImages.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                image_map[int(row['bookCode'])] = row['image']
            except KeyError as e:
                print(f"KeyError: {e}. Row: {row}")

    # Add the image_url to the product
    if product.bookCode in image_map:
        product.image_url = image_map[product.bookCode]
    else:
        product.image_url = None

    # Cek apakah 'last_login' ada dalam cookies
    last_login = request.COOKIES.get('last_login')

    context = {
        'name': request.user.username if request.user.is_authenticated else None,
        'last_login': last_login,
        'product': product,
    }

    return render(request, 'product_details.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun kamu sudah berhasil dibuat!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            last_login_time = datetime.datetime.now().replace(microsecond=0)
            formatted_last_login = last_login_time.strftime('%Y-%m-%d %H:%M:%S')
            response.set_cookie('last_login', formatted_last_login)
            return response
        else:
            messages.info(request, 'Maaf, username atau password yang anda berikan salah. Mohon coba lagi! :D')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order = Order.objects.get(user=request.user, ordered=False)
    order_item = OrderItem.objects.get(order=order, product=product)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return redirect('cart_view')

@login_required
def cart_view(request):
    order = Order.objects.get(user=request.user, ordered=False)
    return render(request, 'cart.html', {'order': order})

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")