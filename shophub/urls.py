
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seller/', include('shop.urls')),
    path('api/buyer/', include('buyer.urls')),
    path('api/account/', include('account.urls'))
]
