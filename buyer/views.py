from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import Product
from buyer.models import Cart
from .serializers import CartSerializer
from shop.serializers import ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from shop.decorators import seller_required, buyer_required



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