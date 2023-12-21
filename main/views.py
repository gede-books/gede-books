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

from main.models import Product, Order, OrderItem, ReviewProduct, Wishlist, WishlistItem
from book.models import Book
from .forms import ReviewForm, SearchForm, CheckoutForm

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

    reviews=ReviewProduct.objects.filter(product=product)

    # Cek apakah 'last_login' ada dalam cookies
    last_login = request.COOKIES.get('last_login')

    context = {
        'name': request.user.username if request.user.is_authenticated else None,
        'last_login': last_login,
        'product': product,
        'reviews': reviews
    }

    return render(request, 'product_details.html', context)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
@csrf_exempt
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    order_item, created_order_item = OrderItem.objects.get_or_create(order=order, product=product)
    if not created_order_item:
        order_item.quantity +=1
    order_item.save()
    return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan ke keranjang'})

@login_required(login_url='/login')
@csrf_exempt
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

def get_item_json(request):
    product_item = Product.objects.all()
    return HttpResponse(serializers.serialize('json', product_item))
    return redirect('/cart')

@login_required(login_url='/login')
@csrf_exempt
def get_cart_json(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = OrderItem.objects.filter(order=order)

        image_map = {}
        with open('main/bookImages.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    image_map[int(row['bookCode'])] = row['image']
                except KeyError as e:
                    print(f"KeyError: {e}. Row: {row}")

        for order_item in order_items:
            if order_item.product.bookCode in image_map:
                order_item.product.image_url = image_map[order_item.product.bookCode]
            else:
                order_item.product.image_url = None

        cart_items = []
        for order_item in order_items:
            cart_item = {
                'id': order_item.product.id,
                'title': order_item.product.title,
                'quantity': order_item.quantity,
                'price': order_item.product.price,
                'total_price': order_item.get_total_price(),
                'image_url': order_item.product.image_url, 
            }
            cart_items.append(cart_item)

        total = order.get_total()

        return JsonResponse({'cart_items': cart_items, 'total': total})
    except Order.DoesNotExist:
        return JsonResponse({'cart_items': [], 'total': 0})

@login_required(login_url='/login')
@csrf_exempt
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

        for order_item in order_items:
            if order_item.product.bookCode in image_map:
                order_item.product.image_url = image_map[order_item.product.bookCode]
            else:
                order_item.product.image_url = None
            order_item.total_price = order_item.get_total_price()

        return render(request, 'cart.html', {'orders': order_items, 'total':total, 'name': request.user.username})
    except:
        return render(request, 'cart.html', {'total':0, 'name': request.user.username})

@login_required(login_url='/login')
@csrf_exempt
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, wishlisted=False)
    wishlist_item, created_wishlist_item = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

    wishlist_item.save()
    return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan ke wishlist'})

@login_required(login_url='/login')
@csrf_exempt
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.get(user=request.user, wishlisted=False)
    wishlist_item = WishlistItem.objects.get(wishlist=wishlist, product=product)
    wishlist_item.delete()
    return redirect('main:wishlist_view')

@login_required(login_url='/login')
@csrf_exempt
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user, wishlisted=False)
        # total = order.get_total()
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

        image_map = {}
        with open('main/bookImages.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    image_map[int(row['bookCode'])] = row['image']
                except KeyError as e:
                    print(f"KeyError: {e}. Row: {row}")

        for wishlist_item in wishlist_items:
            if wishlist_item.product.bookCode in image_map:
                wishlist_item.product.image_url = image_map[wishlist_item.product.bookCode]
            else:
                wishlist_item.product.image_url = None
            # wishlist_item.total_price = wishlist_item.get_total_price()

        # return render(request, 'cart.html', {'orders': order_items, 'total':total, 'name': request.user.username})
        return render(request, 'wishlist.html', {'wishlists': wishlist_items, 'name': request.user.username})
    except:
        # return render(request, 'cart.html', {'total':0, 'name': request.user.username})
        return render(request, 'wishlist.html', {'name': request.user.username})
    
@login_required(login_url='/login/')
@csrf_exempt
def get_wishlist_json(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user, wishlisted=False)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

        image_map = {}
        with open('main/bookImages.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    image_map[int(row['bookCode'])] = row['image']
                except KeyError as e:
                    print(f"KeyError: {e}. Row: {row}")

        for wishlist_item in wishlist_items:
            if wishlist_item.product.bookCode in image_map:
                wishlist_item.product.image_url = image_map[wishlist_item.product.bookCode]
            else:
                wishlist_item.product.image_url = None

        wishlists_items = []
        for wishlist_item in wishlist_items:
            wishlist_item = {
                'id': wishlist_item.product.id,
                'title': wishlist_item.product.title,
                'image_url': wishlist_item.product.image_url, 
            }
            wishlists_items.append(wishlist_item)

        return JsonResponse({'wishlists_items': wishlists_items})
    except Order.DoesNotExist:
        return JsonResponse({'wishlists_items': []})

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

@login_required(login_url='/login')
@csrf_exempt
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

@login_required(login_url='/login')
@csrf_exempt
def checkout_cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order.ordered = True
    order.save()
    return redirect('/purchased_books')

@login_required(login_url='/login')
@csrf_exempt
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            payment_method = form.cleaned_data.get('payment_method')

            context = {
                'name': request.user.username if request.user.is_authenticated else None,
                'address': address,
                'payment_method': payment_method,
                'is_submitted': True
            }
            try:
                current_order = Order.objects.get(user=request.user, ordered=False)
                current_order_items = OrderItem.objects.filter(order=current_order)
                current_order.ordered = True
                current_order.save()

            except Order.DoesNotExist:
                pass
            return render(request, 'checkout.html', context)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

@login_required(login_url='/login')
def purchased_books(request):
    last_login = request.COOKIES.get('last_login', 'Not available')
    return render(request, 'purchased_books.html', {'name': request.user.username, 'last_login': last_login})
                    
@login_required(login_url='/login')
@csrf_exempt
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
                image_url = image_map[order_item.product.bookCode].rstrip()
            else:
                image_url = None
            
            try:
                ReviewProduct.objects.get(user=request.user, product=order_item.product)
                reviewed = True
            except:
                reviewed = False

            book_data = {
                'id': order_item.product.id,
                'title': order_item.product.title,
                'price': order_item.product.price,
                'category': order_item.product.category,
                'rating': order_item.product.rating,
                'image_url': image_url,
                'reviewed': reviewed,
            }

            purchased_books.append(book_data)
            
    return JsonResponse({'order_items': purchased_books, 'name': request.user.username})

@login_required(login_url='/login')
@csrf_exempt
def tinggalkan_review(request, id):
    form = ReviewForm(request.POST or None)
    product = get_object_or_404(Product, pk=id)
    
    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.timestamp = datetime.datetime.now()
        review.save()
        product.update_average_rating()
        return HttpResponseRedirect(reverse('main:purchased_books'))
    
    last_login = request.COOKIES.get('last_login', 'Not available')

    context = {
        'form': form,
        'product': product,
        'last_login': last_login
    }

    return render(request, 'tinggalkan_review.html', context)

@login_required(login_url='/login')
@csrf_exempt
def tinggalkan_review_flutter(request, id):
    try:
        data = request.body.decode('utf-8')
        until = len(data) - 2
        product = get_object_or_404(Product, pk=id)
        review = ReviewForm().save(commit=False)
        review.rating = data[10:11]
        review.review = data[24:until]
        review.product = product
        review.user = request.user
        review.timestamp = datetime.datetime.now()
        review.save()
        product.update_average_rating()
        return JsonResponse('Success', status=200, safe=False)
    except:
        return JsonResponse('Failed', status=404, safe=False)