from django.contrib import admin
from account.models import BuyerProfile, SellerProfile, UserProfile, Notification

# Register your models here.
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(UserProfile)
admin.site.register(Notification)