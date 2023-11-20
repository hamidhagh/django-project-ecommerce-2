from django.db import models
from django.contrib.auth.models import User
from home.models import Product,ProductLine


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=1000)
    code = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.user.username
    

    def get_total_price(self):
        total = sum(i.total_price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_user')
    product = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_product')
    product_line = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='order_product_line')
    quantity = models.IntegerField()


    def __str__(self):
        return self.user.username
    

    def size(self):
        return self.product_line.size.name
    

    def color(self):
        return self.product_line.color.name
    

    def total_price(self):
        if self.product.status != 'None':
            return self.product_line.sale_price * self.quantity
        else:
            return self.product.sale_price * self.quantity

    

class DiscountCode(models.Model):
    code = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    discount = models.IntegerField()
