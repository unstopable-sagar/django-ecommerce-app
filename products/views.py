from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.auth import admin_only

# Create your views here.
def index(request):
    categories = Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'products/index.html',context)

def show_category_products(request,category_id):
    category=Category.objects.get(id=category_id)
    products=Product.objects.filter(category=category)
    context={
        'products':products,
        'category':category
    }
    return render(request,'products/products.html',context)

def product_details(request,product_id):
    product=Product.objects.get(id=product_id)
    context={
        'product':product
    }
    return render(request,'products/productdetails.html',context)

@login_required
@admin_only
def show_category(request):
    context={
        'category':Category.objects.all()
    }
    return render(request,'products/categories.html',context)

@login_required
@admin_only
def add_product(request):
    if request.method == 'POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product added')
            return redirect('/category/products/addproduct')
        else:
            messages.add_message(request,messages.ERROR,'please verify form fields')
            return render(request,'products/addproduct.html',{'form':form})
    context={
        'form':ProductForm
    }
    return render(request,'products/addproduct.html',context)

@login_required
@admin_only
def add_category(request):
    if request.method == 'POST':
        form=CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'category added')
            return redirect('/categories/addcategory')
        else:
            messages.add_message(request,messages.ERROR,'please verify form fields')
            return render(request,'products/addcategory.html',{'form':form})
    context={
        'form':CategoryForm
    }
    return render(request,'products/addcategory.html',context)

@login_required
@admin_only
def delete_product(request,product_id,category_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request,messages.SUCCESS,'product deleted successfully')
    return redirect('/category/<int:category_id>/products')

@login_required
@admin_only
def delete_category(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request,messages.SUCCESS,'category deleted successfully')
    return redirect('/categories')

@login_required
@admin_only
def update_product(request,product_id):
    instance=Product.objects.get(id=product_id)
    if request.method == 'post':
        form=ProductForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product updated')
            return redirect('/product/<int:product_id>')
        else:
            messages.add_message(request,messages.ERROR,'please verify form fields')
            return render(request,'products/updateproduct.html',{'form':form})
    context={
        'form':ProductForm(instance=instance)
    }
    return render(request,'products/updateproduct.html',context)

@login_required
@admin_only
def update_category(request,category_id):
    instance=Category.objects.get(id=category_id)
    if request.method == 'POST':
        form=CategoryForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'category updated')
            return redirect('/categories')
        else:
            messages.add_message(request,messages.ERROR,'please verify form fields')
            return render(request,'products/updatecategory.html',{'form':form})
    context={
        'form':CategoryForm(instance=instance)
    }
    return render(request,'products/updatecategory.html',context)

