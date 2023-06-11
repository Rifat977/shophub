from django.urls import path
from buyer.views import ProductListAPIView, ProductRetrieveAPIView, AddToCartAPIView, CartView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-retrive'),
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart-view/', CartView.as_view(), name='cart-view'),
]
