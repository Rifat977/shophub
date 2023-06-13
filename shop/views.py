from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from shop.models import Category, Product
from buyer.models import Invoice
from account.models import Notification, UserProfile
from .models import SellerFollow
from buyer.serializers import InvoiceSerializer
from shop.serializers import CategorySerializer, ProductSerializer
from .decorators import seller_required, buyer_required

# All Cateogries
class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# ALl Products of this seller
class Products(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def get(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# Single Product
class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    @seller_required
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save(seller=request.user)

            followed_users = SellerFollow.objects.all()

            for seller_follow in followed_users:
                user = seller_follow.follower.user_profile.user
                message = f"{product.name} has been added to {request.user.username}'s shop"
                notification = Notification.objects.create(user=user, message=message, notification_type="for_seller")


            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUD(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @seller_required
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @seller_required
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InvoiceListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def get(self, request):
        invoices = Invoice.objects.filter(seller=request.user)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

class InvoiceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk, seller=request.user)
        except Invoice.DoesNotExist:
            raise NotFound("Invoice not found")

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

class ChangeToBuyerModeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def post(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise NotFound("User not found")

        if user_profile.current_mode == "buyer":
            user_profile.current_mode = "seller"
        else:
            user_profile.current_mode = "buyer"

        user_profile.save()

        return Response({"message": "Your current mode has been changed."})