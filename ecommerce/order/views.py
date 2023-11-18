from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import Order, OrderItem, DiscountCode
from .forms import OrderForm, DiscountCodeForm
from cart.models import Cart


@login_required(login_url='user_login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = DiscountCodeForm()
    context = {'order':order,'form':form}
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
            


@require_POST
def discount_code(request, order_id):
    form = DiscountCodeForm(request.POST)
    time = timezone.now
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            discount_code = DiscountCode.objects.get(code__iexact=code, start_time__lte=time, end_time__gte=time, is_active=True)
        except DiscountCode.DoesNotExist:
            messages.error(request, 'wrong code!', 'danger')
            return redirect('order-detail', order_id)
        
        order = Order.objects.get(id=order_id)
        order.discount = discount_code.discount
        order.save()

    return redirect('order-detail', order_id)

