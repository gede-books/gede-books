from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from main.models import Product, Order, OrderItem
from book.models import Book

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
        products.append(product)

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
        'products': products
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
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
            return redirect('main:show_main')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout(request):
    logout(request)
    return redirect('main:login')

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