from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('update/', views.user_update, name='user_update'),
    path('change_password/', views.change_password, name='change_password'),
    # path('login_phone/', views.login_phone, name='login_phone'),
    # path('phone_verify/', views.phone_verify, name='phone_verify'),
]
