from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'modified_time')
    list_filter = ('created_time',)
    prepopulated_fields = {'slug':('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','discount','sale_price','amount','available', 'created_time', 'modified_time')
    list_filter = ('available',)
    prepopulated_fields = {'slug':('name',)}



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product)
