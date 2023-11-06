from django.shortcuts import render
from .models import Category



def home(request):
    # category = Category.objects.all()
    # context = {'category':category}
    return render(request, 'home/home.html')


def all_products(request):
    return render(request, 'home/products.html')
