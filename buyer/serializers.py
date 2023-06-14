from rest_framework import serializers
from shop.serializers import ProductSerializer
from buyer.models import Cart, Invoice
from shop.models import BuyerReview

class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'products', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        cart = Cart.objects.create(**validated_data)
        for product_data in products_data:
            cart.products.add(product_data)
        return cart

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        instance.products.set(products_data)
        return instance

class InvoiceSerializer(serializers.ModelSerializer):
    purchases = serializers.StringRelatedField(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_id', 'buyer', 'seller', 'payment_intent_id', 'purchase_date', 'address', 'status', 'total_price', 'purchases']
        read_only_fields = ['id', 'invoice_id', 'buyer', 'seller', 'payment_intent_id', 'purchase_date', 'status', 'total_price', 'purchases']


class BuyerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerReview
        fields = ('id', 'buyer', 'product', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'buyer', 'product', 'created_at')
