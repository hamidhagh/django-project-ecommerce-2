from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')


def all_products(request):
    return render(request, 'home/products.html')
