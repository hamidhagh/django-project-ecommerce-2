from django.contrib import admin
from .models import Category, Product, ProductLine, Size, Color


class ProductLineInline(admin.TabularInline):
    model = ProductLine
    #extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'modified_time','parent')
    list_filter = ('created_time',)
    prepopulated_fields = {'slug':('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','discount','sale_price','amount','available', 'created_time', 'modified_time')
    list_filter = ('available',)
    list_editable = ('amount',)
    prepopulated_fields = {'slug':('name',)}
    raw_id_fields = ('category',)
    inlines = [ProductLineInline]



admin.site.register(Category,CategoryAdmin)
admin.site.register(Product)
admin.site.register(ProductLine)
admin.site.register(Size)
admin.site.register(Color)
