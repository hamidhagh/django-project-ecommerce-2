from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.all_products, name='all_products'),
    path('product-info/<slug:slug>/', views.product_info, name='product_info'),
    path('category/<slug:slug>/<int:id>/', views.all_products, name='category'),
]
