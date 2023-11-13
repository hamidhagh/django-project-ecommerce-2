from django.db import models
from django.contrib.auth.models import User
from home.models import Product,ProductLine


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username
    

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
    

