from django.shortcuts import render,get_object_or_404
from .models import Product
from datetime import datetime

# Create your views here.

def products(request):
    pro=Product.objects.all()
    name=None
    if 'searchname' in request.GET:
        name=request.GET['searchname']
        if name:
            pro=pro.filter(name__icontains=name)

    if 'searchdesc' in request.GET:
        desc=request.GET['searchdesc']
        if desc:
            pro=pro.filter(description__icontains=desc)

    if 'searchpricemin' in request.GET and 'searchpricemax' in request.GET:
        min = request.GET['searchpricemin']
        max= request.GET['searchpricemax']
        if min and max :
            pro=pro.filter(price__gte=min,price__lte=max)


    context = {
        'product' : pro
       
    }
    return render(request,'products/products.html', context)

def product(request,pro_id):
    context = {
        'pro' : get_object_or_404(Product, pk=pro_id)
    }
    return render(request,'products/product.html',context)

def search(request):
    return render(request,'products/search.html')