from django.db import models
from django.contrib.auth.models import User
from home.models import *



class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_line = models.ForeignKey(ProductLine,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField()
