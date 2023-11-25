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






#######

# {% extends "home/base.html" %}
# {% block title %} 
# cart
# {% endblock %}
# {% block body %}
# <h1>cart</h1>

#     <div class="container">
#         <div class="row">

#             <table class="table">
#                 <thead>
#                     <tr>
#                         <th scope="col">#</th>
#                         <th scope="col">image</th>
#                         <th scope="col">product</th>
#                         <th scope="col">size</th>
#                         <th scope="col">color</th>
#                         <th scope="col">price</th>
#                         <th scope="col">quantity</th>
#                         <th scope="col">total price</th>
#                         <th scope="col">delete</th>
#                     </tr>
#                     </thead>
#                     <tbody>


#                     {% for crt in cart %}   
#                     <tr>
#                         <th scope="row">{{ forloop.counter }}</th>
#                         <td><img src="{{ crt.product.image.url }}" style="width:100px" alt=""></td>
#                         <td>{{ crt.product.name }}</td>
#                         <td>{{ crt.product_line.size }}</td>
#                         <td>{{ crt.product_line.color }}</td>
#                         <td>
#                             {% if crt.product.status != 'None' %}
#                                 {{ crt.product_line.sale_price }}
#                             {% else %}
#                                 {{ crt.product.sale_price }}
#                             {% endif %}
#                         </td>
#                         <td>
#                             <a href="{% url 'card-sub-update' crt.id %}"><i class="fa fa-minus"></i></a>
#                             {{ crt.quantity }}
#                             <a href="{% url 'card-add-update' crt.id %}"><i class="fa fa-plus"></i></a>
                            
#                         </td>
#                         <td>
#                             {% if crt.product.status != 'None' %}
#                                 {% widthratio crt.product_line.sale_price 1 crt.quantity %}
#                             {% else %}
#                                 {% widthratio crt.product.sale_price 1 crt.quantity %}
#                             {% endif %}
#                         </td>
#                         <td>
#                             <a href="{% url 'cart-remove' crt.id %}"><i class="fa fa-trash" style="color:red"></i></a>
#                         </td>
#                     </tr>
#                     {% endfor %}
#                     <tr>
#                         <td colspan="7">total</td>
#                         <td>{{ total }}</td>


#                 </tbody>
#             </table>
#         </div>
#         <div class="row">
#             <form method="post" action="{% url 'order-create' %}">
#                 {% csrf_token %}
#                 <div class="card" style="padding:10px">
#                     <label for="">email:
#                         <input type="email" name="email" value="{{ user.email }}" required>
#                     </label>
#                     <label for="">first name:
#                         <input type="text" name="first_name" value="{{ user.first_name }}" required>
#                     </label>
#                     <label for="">last_name:
#                         <input type="text" name="last_name" value="{{ user.last_name }}" required>
#                     </label>
#                     <label for="">address:
#                         <input type="text" name="address" value="{{ user.profile.address }}" required>
#                     </label>
                    
#                 </div>
#                 <br>
#                 <button type="submit" class="btn btn-outline-danger">order</button>
#             </form>
#         </div>




#     </div>







# {% endblock %}