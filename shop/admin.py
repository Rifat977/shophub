from django.contrib import admin
from .models import Category, Product, Invitation, BuyerReview

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Invitation)
admin.site.register(BuyerReview)