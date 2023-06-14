import uuid
import stripe
from stripe.error import StripeError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from shop.models import Product, SellerFollow
from buyer.models import Cart
from .models import Invoice, Purchase, Cart
from account.models import BuyerProfile, SellerProfile, Notification
from .serializers import CartSerializer, InvoiceSerializer
from shop.serializers import ProductSerializer
from shop.decorators import seller_required, buyer_required
from django.shortcuts import get_object_or_404


stripe.api_key = 'rk_test_51NIYblLZhXDvAtyNAM1wqEffqzn0uY0T2OtaaKUR1wZ4h6EwZ2dWUAbsiQIhQcFdUaPw742ioHcBbVS3BRJWWlQV00RPyOTRNZ'


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @buyer_required
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @buyer_required
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @buyer_required
    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    @buyer_required
    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = None

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class FollowSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, seller_id):
        buyer_profile = get_object_or_404(BuyerProfile, user_profile__user=request.user)
        seller = get_object_or_404(SellerProfile, id=seller_id)

        if SellerFollow.objects.filter(follower=buyer_profile, seller=seller).exists():
            return Response({'message': 'You are already following this seller.'})

        follow = SellerFollow(follower=buyer_profile, seller=seller)
        follow.save()

        message = f'{buyer_profile.user_profile.user.username} started following you.'
        notification = Notification(user=seller.user_profile.user, message=message, notification_type='for_seller')
        notification.save()

        return Response({'message': 'You are now following the seller.'})

    def delete(self, request, seller_id):
        buyer_profile = get_object_or_404(BuyerProfile, user_profile__user=request.user)
        seller = get_object_or_404(SellerProfile, id=seller_id)

        follow = SellerFollow.objects.filter(follower=buyer_profile, seller=seller).first()
        if not follow:
            return Response({'message': 'You are not following this seller.'})

        follow.delete()
        return Response({'message': 'You have unfollowed the seller.'})


# product order
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @buyer_required
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class ProductPurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @buyer_required
    def post(self, request):
        address = request.data.get('address', '')
        payment_method = request.data.get('payment_method')

        if not payment_method:
            raise APIException('Payment method is required.')

        try:
            cart = Cart.objects.get(user=request.user)

            if not cart.products.exists():
                raise APIException('No items in the cart.')

            purchases = []
            total_price = 0

            for product in cart.products.all():
                purchase = Purchase(product=product, price=product.price, buyer=request.user)
                purchase.save()
                purchases.append(purchase)
                total_price += product.price

            invoice_id = uuid.uuid4().hex.upper()[:10]
            invoice = Invoice(buyer=request.user, invoice_id=invoice_id, total_price=total_price, address=address)

            seller = cart.products.first().seller
            invoice.seller = seller
            invoice.save()
            invoice.purchases.set(purchases)

            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='usd',
                payment_method=payment_method,
                confirm=True
            )

            invoice.payment_intent_id = payment_intent.id
            invoice.save()

            cart.products.clear()

            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)

        except Cart.DoesNotExist:
            raise APIException('Cart does not exist.')
        except StripeError as e:
            error_message = str(e)
            raise APIException(error_message)


class ProductOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @buyer_required
    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, id=pk)
        payment_method = request.data.get('payment_method')

        if not payment_method:
            raise APIException('Payment method is required.')

        try:
            payment_intent = stripe.PaymentIntent.confirm(
                invoice.payment_intent_id,
                payment_method=payment_method
            )

            if payment_intent.status == 'succeeded':
                invoice.status = 'paid'
            else:
                invoice.status = 'failed'
            invoice.save()

            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)

        except StripeError as e:
            error_message = str(e)
            raise APIException(error_message)

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @buyer_required
    def get(self, request):
        invoices = Invoice.objects.filter(buyer=self.request.user)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

class InvoiceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @buyer_required
    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk, buyer=request.user)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)