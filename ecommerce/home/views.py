from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductLine



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


def product_info(request,id):
    product = get_object_or_404(Product,id=id)
    if product.status != 'None':
        if request.method == 'POST':
            product_line = ProductLine.objects.filter(product_id=id)
            pl_id = request.POST.get('select')
            chosen_product_line = ProductLine.objects.get(id=pl_id)
        else:
            product_line = ProductLine.objects.filter(product_id=id)
            chosen_product_line = ProductLine.objects.get(id=product_line[0].id)
        context = {'product':product,'product_line':product_line,'chosen_product_line':chosen_product_line}
        return render(request, 'home/product_info.html', context)
    else:

        return render(request, 'home/product_info.html', {'product':product})
