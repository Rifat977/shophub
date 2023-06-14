from rest_framework import serializers
from shop.models import Category, Product, SellerFollow, Invitation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'seller']

    def create(self, validated_data):
        seller = self.context['request'].user
        validated_data['seller'] = seller
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class SellerFollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()

    class Meta:
        model = SellerFollow
        fields = ['id', 'seller', 'follower']


class InvitationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.user.username')
    recipient = serializers.ReadOnlyField(source='recipient.user.username')

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'created_at', 'accepted']

