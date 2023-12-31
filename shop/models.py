from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class BuyerReview(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer.username} for {self.product.name}"


class SellerFollow(models.Model):
    follower = models.ForeignKey('account.BuyerProfile', on_delete=models.CASCADE, related_name='follower')
    seller = models.ForeignKey('account.SellerProfile', on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'seller']

    def __str__(self):
        return f"{self.follower.user_profile.user.username} follows {self.seller.user_profile.user.username}"


class Invitation(models.Model):
    sender = models.ForeignKey('account.SellerProfile', on_delete=models.CASCADE, related_name='invitations_sent')
    recipient = models.ForeignKey('account.SellerProfile', on_delete=models.CASCADE, related_name='invitations_received')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Invitation from {self.sender.user_profile.user.username} to {self.recipient.user_profile.user.username}'
