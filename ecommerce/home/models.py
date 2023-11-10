from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True,related_name='sub')
    sub_category = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[self.slug, self.id])
    



class Product(models.Model):
    
    VARIANT = (
        ('None','none'),
        ('size','size'),
        ('color','color'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True,blank=True)
    sale_price = models.PositiveIntegerField()
    description = RichTextUploadingField(null=True,blank=True)
    image = models.ImageField(upload_to='product')
    status = models.CharField(max_length=255,null=True,blank=True,choices=VARIANT)
    available = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.ImageField(default=0)
    dislike = models.ManyToManyField(User, blank=True, related_name='product_dislike')
    total_dislike = models.ImageField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    @property
    def sale_price(self):
        if not self.discount:
            return self.price
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        return self.sale_price
    

    def total_like(self):
        return self.like.count()
    

    def total_dislike(self):
        return self.dislike.count()
    

    def get_absolute_url(self):
        return reverse('product_info', args=[self.slug])
    

class Size(models.Model):
    name = models.CharField(max_length=100)


class Color(models.Model):
    name = models.CharField(max_length=100)


class ProductLine(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True,blank=True)
    sale_price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
    @property
    def sale_price(self):
        if not self.discount:
            return self.price
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        return self.sale_price