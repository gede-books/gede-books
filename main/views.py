from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.http import JsonResponse

from main.models import Product, Order, OrderItem
from book.models import Book
from main.forms import CheckoutForm

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

    last_login = request.COOKIES.get('last_login', 'Not available')

    context = {
        'name': request.user.username,
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
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    
    return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan ke keranjang'})

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
    return redirect('main:cart_view')

@login_required
def cart_view(request):
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    context = {
        'name': request.user.username,
        'order': order
    }
    return render(request, 'cart.html', context)

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

@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            payment_method = form.cleaned_data.get('payment_method')

            response_text = f"Terima kasih, {name}!\n"
            response_text += f"Detail pemesanan Anda:\n"
            response_text += f"Alamat Pengiriman: {address}\n"
            response_text += f"Metode Pembayaran: {payment_method}\n"
            response_text += "Pesanan Anda sedang diproses. Silakan cek email Anda untuk informasi lebih lanjut."

            return HttpResponse(response_text, content_type='text/plain')
    else:
        form = CheckoutForm()
    
    context = {
        'checkout_form': form
    }

    return render(request, 'cart.html', context)

@login_required
def update_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('new_quantity'))

        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_item = order.orderitem_set.get(product_id=item_id)
            order_item.quantity = new_quantity
            order_item.save()
            return JsonResponse({'status': 'success', 'new_quantity': new_quantity})
        except:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)