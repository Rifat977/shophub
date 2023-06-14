from django.urls import path
from buyer.views import *

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-retrive'),
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart-view/', CartView.as_view(), name='cart-view'),
    path('follow/<int:seller_id>/', FollowSellerView.as_view(), name='follow-seller'),
    path('unfollow/<int:seller_id>/', FollowSellerView.as_view(), name='unfollow-seller'),

    path('purchase/', ProductPurchaseAPIView.as_view(), name='product-purchase'),
    path('product-list/', ProductListAPIView.as_view(), name='product-list'),
    path('order/<int:pk>/', ProductOrderAPIView.as_view(), name='order-product'),

    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice-detail'),

    path('review/', BuyerReviewCreateAPIView.as_view(), name='product-review'),
]
