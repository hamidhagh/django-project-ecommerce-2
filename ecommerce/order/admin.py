from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'product_line', 'size', 'color', 'quantity', 'total_price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'address', 'create_time', 'paid', 'get_total_price', 'code']
    inlines = [OrderItemInline]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_time', 'end_time', 'discount', 'is_active']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(DiscountCode,DiscountCodeAdmin)
