from django.shortcuts import render
from main.models import Product, Order, OrderItem
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.all()
    context = {
        'title': 'Anoooooomgh',
        'language': 'Zimbabwe',
        'firstName': 'Rakha',
        'lastName': 'Abid'
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