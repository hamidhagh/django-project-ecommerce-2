from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:id>/', views.cart_add, name='cart-add'),
    path('delete/<int:id>/', views.cart_delete, name='cart-delete'),

]

