from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.all_products, name='all_products'),
    path('product-info/<int:id>/', views.product_info, name='product_info'),
    path('category/<int:id>/', views.all_products, name='category'),
    path('like/<int:id>/', views.product_like, name='product-like'),
    path('dislike/<int:id>/', views.product_dislike, name='product-dislike'),
    path('product-info/<int:id>/comment/', views.product_comment, name='product-comment'),
    path('product-info/<int:id>/comment/<int:comment_id>/reply/', views.product_comment_reply, name='product-comment-reply'),
    path('comment/<int:id>/like/', views.product_comment_like, name='product-comment-like'),
    path('search/', views.product_search, name='product-search'),
]






# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('product/', views.all_products, name='all_products'),
#     path('product-info/<int:id>/', views.product_info, name='product_info'),
#     path('category/<int:id>/', views.all_products, name='category'),
#     path('like/<int:id>/', views.product_like, name='product-like'),
#     path('dislike/<int:id>/', views.product_dislike, name='product-dislike'),
#     path('product-info/<int:id>/comment/', views.product_comment, name='product-comment'),
#     path('product-info/<int:id>/comment/<int:comment_id>/reply/', views.product_comment_reply, name='product-comment-reply'),
#     path('product-info/<int:id>/comment/<int:comment_id>/like/', views.product_comment_like, name='product-comment-like'),
# ]

