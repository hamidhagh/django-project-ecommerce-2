from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.db.models.signals import post_save

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
        return reverse('category', args=[self.id])
    


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    
    VARIANT = (
        ('None','none'),
        ('size','size'),
        ('color','color'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    chart_change = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(null=True,blank=True)
    sale_price = models.PositiveIntegerField()
    description = RichTextUploadingField(null=True,blank=True)
    image = models.ImageField(upload_to='product')
    color = models.ManyToManyField('Color', blank=True)
    size = models.ManyToManyField('Size', blank=True)
    status = models.CharField(max_length=255,null=True,blank=True,choices=VARIANT)
    available = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.ImageField(default=0)
    dislike = models.ManyToManyField(User, blank=True, related_name='product_dislike')
    total_dislike = models.ImageField(default=0)
    favorite = models.ManyToManyField(User, blank=True, related_name='user_favorite')
    total_favorite = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    change = models.BooleanField(default=False)
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
    

    def average(self):
        data = Comment.objects.filter(is_reply=False,product=self).aggregate(avg=models.Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'],1)
        return star


    def total_like(self):
        return self.like.count()
    

    def total_dislike(self):
        return self.dislike.count()
    

    def get_absolute_url(self):
        return reverse('product_info', args=[self.id])
    

class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductLine(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    chart_change = models.BooleanField(default=False)
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


    # def get_absolute_url(self):
    #     return reverse('product_info', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    created_time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    like = models.ManyToManyField(User,blank=True,related_name='comment_like')
    like_number = models.PositiveIntegerField(default=0)


    def like_number(self):
        return self.like.count()


    def __str__(self):
        return self.product.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='image/',blank=True)




class Chart(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    price = models.IntegerField(default=0)
    modified_time = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    size = models.CharField(max_length=100,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name='product_update')
    product_line = models.ForeignKey(ProductLine,on_delete=models.CASCADE,null=True,blank=True,related_name='product_line_update')



    def __str__(self):
        return self.name
    



def product_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    if data.chart_change == True:
        Chart.objects.create(product=data,price=data.price,modified_time=data.modified_time,name=data.name)


post_save.connect(product_post_save,sender=Product)



def product_line_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    if data.chart_change == True:
        Chart.objects.create(product_line=data,price=data.price,modified_time=data.modified_time,name=data.name,size=data.size,color=data.color)


post_save.connect(product_line_post_save,sender=Product)



class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.product.name
