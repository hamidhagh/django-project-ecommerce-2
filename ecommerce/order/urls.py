from django.urls import path
from . import views

urlpatterns = [
    path('<int:order_id>/', views.order_detail, name='order-detail'),
    path('create/', views.order_create, name='order-create'),
    path('discount-code/<int:order_id>/', views.discount_code, name='discount-code'),

]

