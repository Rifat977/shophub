from django.urls import path
from buyer.views import ProductListAPIView, ProductRetrieveAPIView, AddToCartAPIView, CartView, FollowSellerView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-retrive'),
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart-view/', CartView.as_view(), name='cart-view'),
    path('follow/<int:seller_id>/', FollowSellerView.as_view(), name='follow-seller'),
    path('unfollow/<int:seller_id>/', FollowSellerView.as_view(), name='unfollow-seller'),
]
