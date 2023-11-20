from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:id>/', views.cart_add, name='cart-add'),
    path('delete/<int:id>/', views.cart_delete, name='cart-delete'),
    path('add_update/<int:id>/', views.cart_add_update, name='cart-add-update'),
    path('sub_update/<int:id>/', views.cart_sub_update, name='cart-sub-update'),
]

