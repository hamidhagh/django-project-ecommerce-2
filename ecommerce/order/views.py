from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import Cart


@login_required(login_url='user_login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order':order}
    return render(request, 'order/order.html', context)



@login_required(login_url='user_login')
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(user_id=request.user.id,email=data['email'],first_name=data['first_name'],
                                 last_name=data['last_name'],address=data['address'])
            
            cart = Cart.objects.filter(user_id=request.user.id)
            for item in cart:
                OrderItem.objects.create(order_id=order.id,user_id=request.user.id,
                                         product_id=item.product_id,product_line_id=item.product_line_id,quantity=item.quantity)
            #Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order-detail', order.id)
            
