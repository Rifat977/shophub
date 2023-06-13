from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class Purchase(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self):
        return f"Purchase of {self.product} by {self.buyer.username}"

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=100, unique=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    purchases = models.ManyToManyField(Purchase, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} for {self.buyer.username}"
