from django.shortcuts import render, redirect
from home.models import Product, ProductLine
from .models import *
from .forms import *
from order.forms import OrderForm



def cart(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    user = request.user
    order_form = OrderForm()
    total = 0
    for item in cart:
        if item.product.status != 'None':
            total += item.product_line.sale_price * item.quantity
        else:
            total += item.product.sale_price * item.quantity

    return render(request, 'cart/cart.html', {'cart':cart,'total':total,'order_form':order_form,'user':user})



def cart_add(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.status != 'None':
        pl_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id, product_line_id=pl_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        pl_id = request.POST.get('select')
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if check == 'yes':
                if product.satus != 'None':
                    item = Cart.objects.get(user_id=request.user.id,product_id=id,product_line_id=pl_id)
                else:
                    item = Cart.objects.get(user_id=request.user.id,product_id=id)

                item.quantity += quantity
                item.save()
            else:
                Cart.objects.create(user_id=request.user.id,product_id=id,product_line_id=pl_id,quantity=quantity)
        
        return redirect(url)
    


def cart_delete(request,id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)





def cart_add_update(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.product.status == 'None':
        product = Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
        
    else:
        product_line = ProductLine.objects.get(id=cart.product_line.id)
        if product_line.amount > cart.quantity:
            cart.quantity += 1
    cart.save()
    return redirect(url)




def cart_sub_update(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)

