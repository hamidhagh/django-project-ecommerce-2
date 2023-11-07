from django.shortcuts import render, get_object_or_404
from .models import Category, Product



def home(request):
    category = Category.objects.filter(sub_category=False)
    context = {'category':category}
    return render(request, 'home/home.html', context)


def all_products(request,slug=None,id=None):
    products = Product.objects.all()
    category = Category.objects.filter(sub_category=False)
    if slug and id:
        data = get_object_or_404(Category,slug=slug)
        products = Product.objects.filter(category=data)

    context = {'products':products, 'category':category}
    return render(request, 'home/products.html', context)


def product_info(request,slug):
    product = get_object_or_404(Product,slug=slug)
    context = {'product':product}
    return render(request, 'home/product_info.html', context)
