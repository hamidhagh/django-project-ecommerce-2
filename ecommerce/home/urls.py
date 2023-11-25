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
    path('favorite/<int:id>/', views.product_favorite, name='product-favorite'),
    path('contact/', views.contact, name='contact'),
    path('compare/<int:id>/', views.compare, name='compare'),
    
    path('compare-add/<int:id>/', views.compare_add, name='compare-add'),
    path('compare-list/', views.compare_list, name='compare-list'),
    path('compare-remove/<int:product_id>/', views.compare_remove, name='compare-remove'),
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

