from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'product_line', 'size', 'color', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'address', 'create_time', 'paid']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
