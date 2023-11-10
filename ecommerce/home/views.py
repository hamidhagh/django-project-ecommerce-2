from django.shortcuts import render, get_object_or_404, redirect
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
    similar = product.tags.similar_objects()[:2]
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_dislike = False
    if product.dislike.filter(id=request.user.id).exists():
        is_dislike = True

    if product.status != 'None':
        if request.method == 'POST':
            product_line = ProductLine.objects.filter(product_id=id)
            pl_id = request.POST.get('select')
            chosen_product_line = ProductLine.objects.get(id=pl_id)
        else:
            product_line = ProductLine.objects.filter(product_id=id)
            chosen_product_line = ProductLine.objects.get(id=product_line[0].id)
        context = {'product':product,'product_line':product_line,'chosen_product_line':chosen_product_line,'similar':similar,'is_like':is_like,'is_dislike':is_dislike}
        return render(request, 'home/product_info.html', context)
    else:

        return render(request, 'home/product_info.html', {'product':product,'similar':similar,'is_like':is_like,'is_dislike':is_dislike})
    


def product_like(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
    else:
        product.like.add(request.user)
        is_like = True
    #return redirect('product_info', product.id)
    #return the same page
    return redirect(url)



def product_dislike(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_dislike = False
    if product.dislike.filter(id=request.user.id).exists():
        product.dislike.remove(request.user)
        is_dislike = False
    else:
        product.dislike.add(request.user)
        is_dislike = True
    #return redirect('product_info', product.id)
    #return the same page
    return redirect(url)
