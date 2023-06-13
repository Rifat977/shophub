from django.urls import path
from shop.views import *

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', Products.as_view(), name='product-list'),
    path('product/<int:id>/', ProductRetrieveAPIView.as_view(), name='product-retrieve'), #get request
    path('product/', ProductCreateAPIView.as_view(), name='product-list'),
    path('edit/product/<int:pk>/', ProductUD.as_view(), name='product-detail'), # put, delete request

    path('orders/', InvoiceListAPIView.as_view(), name='invoice-list'),
    path('orders/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice-detail'),

    path('change-mode/', ChangeToBuyerModeAPIView.as_view(), name='change-mode'),

]
