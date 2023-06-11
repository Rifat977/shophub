from django.contrib.auth.models import User
from django.db import models
from shop.models import Product

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    current_mode = models.CharField(max_length=6, default='buyer')

    def __str__(self):
        return self.user.username

class SellerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    invited_sellers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='invited_by')

    def __str__(self):
        return self.user_profile.user.username

class BuyerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Product, blank=True)
    favorite_shops = models.ManyToManyField(SellerProfile, related_name='followers', blank=True)

    def __str__(self):
        return self.user_profile.user.username