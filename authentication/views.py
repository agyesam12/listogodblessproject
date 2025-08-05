from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
import json
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from .forms import  CreateUserAccount
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       # items = order.orderitem_set.all()
        cart_item = order.get_cart_items
    else:
        order = {'get_carttotal':0,'get_cart_items':0}
        items = []
        cart_item = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products,'order':order,'cart_item':cart_item}
    return render(request, 'store.html', context)




@login_required
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_item = order.get_cart_items
    context = {'items': items, 'order': order,'cart_item':cart_item}
    return render(request, 'cart.html', context)


@login_required
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_item = order.get_cart_items
    context = {'items': items, 'order': order,'cart_item':cart_item}
    return render(request, 'checkout.html', context)



@login_required
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was updated', safe=False)




def signup(request):
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        form = CreateUserAccount(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            customer = Customer.objects.create(user=user)
            messages.success(request, f"Acount created sucessfully....")
            return redirect("signin")
        else:
            print("Something went wrong")
    else:
        form = CreateUserAccount()
    context = {'form':form}
    return render(request, 'signup.html',context)


def signin(request):
    if request.method == 'POST':
        n =request.POST['username']
        p = request.POST['password']
        try:
            if User.objects.filter(username=n).exists():
                user = User.objects.get(username=n)
                if user.is_active:
                    user = authenticate(request, username=n,password=p)
                    login(request, user)
                    return redirect("store")
                else:
                    user_one = authenticate(request, username=n,password=p)
                    if user_one is not None: 
                        login(request, user_one)
                    else:
                        print("Something went wrong ..")
                        messages.info(request,f"Contact your programmers for more info....")
            else:
                messages.info(request,f"Account not found")
        except(User.DoesNotExist):
            user = None
            print("User is none")
    return render(request,'signin.html')


def signout(request):
    logout(request)
    return redirect('store')


def user_dashboard(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        print("user is not logged in")
    context={
        
        'order':order,
        'items':items
    }
    return render(request, 'user_dashboard.html')