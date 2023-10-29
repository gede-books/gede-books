from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse

from main.models import Product, Order, OrderItem
from book.models import Book

import datetime
import csv


@login_required(login_url='/login')
def show_main(request):
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

    # Jika ada parameter kategori, filter produk berdasarkan kategori tersebut
    selected_category = request.GET.get('category')
    if selected_category:
        products = [product for product in products if selected_category in product.category.split('; ')]

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
        'selected_category': selected_category
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
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

    context = {
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],
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
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Maaf, username atau password kamu salah. Silahkan coba lagi.')
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
    order_item, created_order_item = OrderItem.objects.get_or_create(order=order, product=product)
    print(created_order_item)
    if not created_order_item:
        order_item.quantity +=1
    order_item.save()
    return redirect('/cart')

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
    return redirect('/cart')

@login_required
def cart_view(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        total = order.get_total()
        order_items = OrderItem.objects.filter(order=order)

        image_map = {}
        with open('main/bookImages.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    image_map[int(row['bookCode'])] = row['image']
                except KeyError as e:
                    print(f"KeyError: {e}. Row: {row}")

        # Add the image_url and total price to the product
        for order_item in order_items:
            if order_item.product.bookCode in image_map:
                order_item.product.image_url = image_map[order_item.product.bookCode]
            else:
                order_item.product.image_url = None
            order_item.total_price = order_item.get_total_price()

        return render(request, 'cart.html', {'orders': order_items, 'total':total, 'name': request.user.username})
    except:
        return render(request, 'cart.html', {'total':0, 'name': request.user.username})


@login_required
def checkout_cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order.ordered = True
    order.save()
    return redirect('/purchased_books')

@login_required
def purchased_books(request):
    return render(request, 'purchased_books.html')
                    
@login_required
def purchased_books_ajax(request):
    orders = Order.objects.filter(user=request.user, ordered=True)
    purchased_books = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            image_map = {}
            with open('main/bookImages.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        image_map[int(row['bookCode'])] = row['image']
                    except KeyError as e:
                        print(f"KeyError: {e}. Row: {row}")

            image_url=None
            if order_item.product.bookCode in image_map:
                image_url = image_map[order_item.product.bookCode]
            else:
                image_url = None

            book_data = {
                'title': order_item.product.title,
                'price': order_item.product.price,
                'category': order_item.product.category,
                'rating': order_item.product.rating,
                'image_url': image_url
            }

            purchased_books.append(book_data)

    return JsonResponse({'order_items': purchased_books, 'name': request.user.username})

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