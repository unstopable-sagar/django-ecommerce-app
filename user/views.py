from django.shortcuts import render,redirect
from products.models import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import LoginForm,ProfileUpdateForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from products.forms import OrderForm
from django.urls import reverse
from django.views import View # class

# Create your views here.
def index(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'userspage/index.html',context)

def show_category_products(request,category_id):
    category=Category.objects.get(id=category_id)
    products=Product.objects.filter(category=category)
    context={
        'products':products,
        'category':category
    }
    return render(request,'userspage/products.html',context)

def product_details(request,product_id):
    product=Product.objects.get(id=product_id)
    context={
        'product':product
    }
    return render(request,'userspage/productdetails.html',context)

def all_products(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'userspage/allproducts.html',context)

def register_user(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'user registered successfully')
            return redirect('/register')
        else:
            messages.add_message(request,messages.ERROR,'please verify form fields')
            return render(request,'userspage/register.html',{'form':form})
    context={
        'form':UserCreationForm
    }
    return render(request,'userspage/register.html',context)  

def login_user(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data # data contains username and password
            user=authenticate(request,username=data['username'],password=data['password'])
        
            if user is not None:
                login(request,user) # user's data is stored in this user
                if user.is_staff:
                    return redirect('/admin/dashboard')
                else:
                    # return redirect('/profile')
                    return redirect('/')
            else:
                messages.add_message(request,messages.ERROR,'please provide correct credentials')
                return render(request,'userspage/login.html',{'form':form})

    context={
        'form':LoginForm
    }
    return render(request,'userspage/login.html',context) 

def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required
def add_to_cart(request,product_id):
    user=request.user
    product=Product.objects.get(id=product_id)

    check_item_presence=Cart.objects.filter(user=user,product=product)
    if check_item_presence:
        messages.add_message(request,messages.ERROR,'Product is already in the cart')
        return redirect('/cart')
    else:
        cart=Cart.objects.create(product=product,user=user)
        if cart:
            messages.add_message(request,messages.SUCCESS,'Product is added to the cart')
            return redirect('/cart')
        else:
            messages.add_message(request,messages.ERROR,'Failed to add item in the cart')
            return redirect('/cart')
        
@login_required
def show_cart(request):
    user=request.user
    cart_items=Cart.objects.filter(user=user)
    context={
        'cart_items':cart_items
    }
    return render(request,'userspage/cart.html',context)

@login_required
def remove_cart_item(request,cart_id):
    cart=Cart.objects.get(id=cart_id)
    cart.delete()
    messages.add_message(request,messages.SUCCESS,'item removed from the cart')
    return redirect('/cart')

@login_required
def post_order(request,product_id,cart_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    cart_item=Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            quantity=request.POST.get('quantity')
            price=product.product_price
            total_price=int(quantity) * int(price)
            contact_no=request.POST.get('contact_no')
            address=request.POST.get('address')
            payment_method=request.POST.get('payment_method')
            payment_status=request.POST.get('payment_status')
            order=Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status
            )
            if order.payment_method=='Cash on delivery':
                cart_item.delete()
                messages.add_message(request,messages.SUCCESS,'Order placed successfully')
                return redirect('/myorder')
            elif order.payment_method=='Esewa':
                return redirect(reverse("esewaform") + "?o_id=" + str(order.id) + "&c_id=" + str(cart_item.id))
            else:
                messages.add_message(request,messages.ERROR,'failed to make an order')
                return render(request,'userspage/orderform.html',{'form':form})
    context={
        'form':OrderForm
    }
    return render(request,'userspage/orderform.html',context)

@login_required
def my_order(request):
    user=request.user
    items=Order.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request,'userspage/myorder.html',context)

@login_required
def remove_order_item(request,order_id):
    item=Order.objects.get(id=order_id)
    item.delete()
    messages.add_message(request,messages.SUCCESS,'order canceled')
    return redirect('/cart')

import hmac
import hashlib # for hashing(transfer, from readable form to unreadable form)(crypto method)
import uuid
import base64

class EsewaView(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        cart=Cart.objects.get(id=c_id)
        order=Order.objects.get(id=o_id)

        uuid_val=uuid.uuid4() # to generate random string

        def generate_sha256(key, message):
            key=key.encode('utf-8')
            message=message.encode('utf-8')

            hmac_sha256=hmac.new(key,message,hashlib.sha256)
            digest=hmac_sha256.digest()
            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        secrete_key='8gBm/:&EnhH.1/q'
        data_to_sign=f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result=generate_sha256(secrete_key, data_to_sign)
        data={
            'amount':order.product.product_price,
            'total_amount':order.total_price,
            'transaction_uuid':uuid_val,
            'product_code':'EPAYTEST',
            'signature':result
        }
        context={
            'order':order,
            'data':data,
            'cart':cart
        }
        return render(request,'userspage/esewa.html',context)
    
import json
@login_required
def esewa_verify(request,order_id,cart_id):
    if request.method == 'GET':
        data=request.GET.get('data') # encoded data
        decoded_data=base64.b64decode(data).decode('utf-8')
        map_data=json.loads(decoded_data)
        order=Order.objects.get(id=order_id)
        cart=Cart.objects.get(id=cart_id)

        if map_data.get('status') == 'COMPLETE':
            order.payment_status=True
            order.save()
            cart.delete()
            messages.add_message(request,messages.SUCCESS,'payment successful')
            return redirect('/myorder')
        else:
            messages.add_message(request,messages.ERROR,'failed to make payment')
            return redirect('/myorder')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form=ProfileUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'profile updated succesfully')
            return redirect('/profile')
        else:
            messages.add_message(request,messages.ERROR,'failed to update profile')
            return render(request,'userspage/updateprofile.html',{'form':form})

    context={
        'form':ProfileUpdateForm(instance=request.user)
    }
    return render(request,'userspage/updateprofile.html',context)

@login_required
def profile(request):
    user=User.objects.get(username=request.user)
    context={
        'user':user
    }
    return render(request,'userspage/profile.html',context)