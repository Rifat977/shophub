from django.urls import path
from account.views import seller_registration, buyer_registration, verify_otp

urlpatterns = [
    path('seller/register/', seller_registration, name='seller_registration'),
    path('buyer/register/', buyer_registration, name='buyer_registration'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    
]
