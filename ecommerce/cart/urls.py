from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_details, name='cart'),
    #path('add/<int:id>/', views.cart_add, name='cart-add'),
    path('add/', views.cart_add, name='cart-add'),
    path('remove/<int:id>/', views.cart_remove, name='cart-remove'),
    path('show/', views.cart_show, name='show'),
    path('add-single/', views.add_single, name='add-single'),
    path('remove-single/', views.remove_single, name='remove-single'),
    #path('sub_update/<int:id>/', views.cart_sub_update, name='cart-sub-update'),
]

