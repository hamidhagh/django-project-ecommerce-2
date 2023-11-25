from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from home.models import ProductLine
from .forms import CartForm
from django.http import JsonResponse


def cart_details(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request):
    product_line_id = request.POST.get('test')
    product_line = get_object_or_404(ProductLine, id=product_line_id)
    cart = Cart(request)
    form = CartForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product_line=product_line, quantity=data['quantity'])
    return redirect('cart')


def cart_remove(request, id):
    product_line = get_object_or_404(ProductLine, id=id)
    cart = Cart(request)
    cart.remove(product_line=product_line)
    return redirect('cart')


def cart_show(request):
    total,price,quantity,discount = 0,0,0,0
    cart = Cart(request)
    for c in cart:
        total += int(c['product_line'].sale_price * c['quantity'])
        price += int(c['product_line'].price * c['quantity'])
        quantity += c['quantity']
        discount = price - total
    response = {'total':total,'price':price,'quantity':quantity,'discount':discount}
    return JsonResponse(response)


def add_single(request):
    product_line_id = request.GET.get('product_line_id')
    product_line = get_object_or_404(ProductLine, id=product_line_id)
    cart = Cart(request)
    cart.add(product_line=product_line, quantity=1)
    cart.save()
    data = {'success': 'ok'}
    return JsonResponse(data)
