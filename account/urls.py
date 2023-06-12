from django.urls import path
from account.views import seller_registration, buyer_registration, verify_otp, JWTLoginView, logout_view, NotificationListView


urlpatterns = [
    path('seller/register/', seller_registration, name='seller_registration'),
    path('buyer/register/', buyer_registration, name='buyer_registration'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', JWTLoginView.as_view(), name='jwt_login'),
    path('logout/', logout_view, name='logout'),

    path('notification/', NotificationListView.as_view(), name='notification'),
]
