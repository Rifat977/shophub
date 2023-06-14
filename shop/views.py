from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import status
from shop.models import Category, Product, Invitation
from buyer.models import Invoice
from account.models import Notification, UserProfile, SellerProfile
from .models import SellerFollow
from buyer.serializers import InvoiceSerializer
from shop.serializers import CategorySerializer, ProductSerializer, SellerFollowSerializer, InvitationSerializer
from account.serializers import UserSerializer
from .decorators import seller_required, buyer_required
from django.shortcuts import get_object_or_404


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


class SellerFollowersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @seller_required
    def get(self, request):
        seller_profile = get_object_or_404(SellerProfile, user_profile__user=request.user)

        followers = SellerFollow.objects.filter(seller=seller_profile)
        serializer = SellerFollowSerializer(followers, many=True)
        return Response(serializer.data)

# invited seller
class InvitationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender = SellerProfile.objects.get(user_profile__user=request.user)
        invitations_sent = Invitation.objects.filter(sender=sender)
        serializer = InvitationSerializer(invitations_sent, many=True)
        return Response(serializer.data)

# invitation detail
class InvitationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        serializer = InvitationSerializer(invitation)
        return Response(serializer.data)

# send invitation
class InvitationSendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender_profile = SellerProfile.objects.get(user_profile__user=request.user)
        recipient_username = request.data.get('recipient')

        if not recipient_username:
            raise APIException('Recipient username is required.')

        try:
            recipient_profile = SellerProfile.objects.get(user_profile__user__username=recipient_username)
        except SellerProfile.DoesNotExist:
            raise APIException('Recipient seller not found.')

        if Invitation.objects.filter(sender=sender_profile, recipient=recipient_profile).exists():
            raise APIException('Invitation already sent to this recipient.')

        invitation = Invitation(sender=sender_profile, recipient=recipient_profile)
        invitation.save()

        serializer = InvitationSerializer(invitation)
        return Response(serializer.data)

# accepted invtation (receiver)
class AcceptedInvitationsReceiverAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipient = SellerProfile.objects.get(user_profile__user=request.user)
        accepted_invitations = Invitation.objects.filter(recipient=recipient, accepted=True)
        senders = [invitation.sender.user_profile.user for invitation in accepted_invitations]
        serializer = UserSerializer(senders, many=True)
        return Response(serializer.data)

# accepted invtations List (Sender)
class AcceptedInvitationsSenderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender = SellerProfile.objects.get(user_profile__user=request.user)
        accepted_invitations = Invitation.objects.filter(sender=sender, accepted=True)
        receivers = [invitation.recipient.user_profile.user for invitation in accepted_invitations]
        serializer = UserSerializer(receivers, many=True)
        return Response(serializer.data)

# accept invite
class InvitationAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_profile = SellerProfile.objects.get(user_profile__user=request.user)
        invitation_id = request.data.get('invitation_id')

        if not invitation_id:
            raise APIException('Invitation ID is required.')

        try:
            invitation = Invitation.objects.get(id=invitation_id, recipient=recipient_profile)
        except Invitation.DoesNotExist:
            raise APIException('Invitation not found.')

        if invitation.accepted:
            raise APIException('Invitation already accepted.')

        sender_profile = invitation.sender
        recipient_profile.invited_sellers.remove(sender_profile)
        recipient_profile.save()

        invitation.accepted = True
        invitation.save()

        return Response({'message': 'Invitation accepted successfully.'})