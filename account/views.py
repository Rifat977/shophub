import random
import string
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from account.models import UserProfile, SellerProfile, BuyerProfile, Notification
from account.serializers import UserSerializer, NotificationSerializer



class JWTLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                profile = user.userprofile
                if not profile.is_verified:
                    return Response({'error': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
            except AttributeError:
                return Response({'error': 'User profile not found'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'detail': 'Successfully logged out.'})

    except Exception as e:
        return Response({'detail': 'Failed to log out.'}, status=400)


@api_view(['POST'])
def seller_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        profile = UserProfile(user=user, current_mode="seller")
        profile.save()
        seller = SellerProfile(user_profile=profile)
        seller.save()
        buyer = BuyerProfile(user_profile=profile)
        buyer.save()

        otp = generate_otp()
        send_otp_email(user.email, otp)

        profile.otp = otp
        profile.save()

        return JsonResponse({'message': 'Seller registered successfully! Please check your email for OTP.'})
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def buyer_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        profile = UserProfile(user=user, current_mode="buyer")
        profile.save()
        buyer = BuyerProfile(user_profile=profile)
        buyer.save()

        otp = generate_otp()
        send_otp_email(user.email, otp)

        profile.otp = otp
        profile.save()

        return JsonResponse({'message': 'Buyer registered successfully! Please check your email for OTP.'})
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(email=email)
        user_profile = user.userprofile 

        if user_profile.is_verified:
            return JsonResponse({'message': 'User is already verified'})

        if user_profile.otp == otp:
            user_profile.is_verified = True
            user_profile.save()
            return JsonResponse({'message': 'OTP verification successful'})
        else:
            return JsonResponse({'message': 'Invalid OTP'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)

def generate_otp():
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(6))
    return otp

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)



class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        user_type = 'buyer' if hasattr(user, 'buyerprofile') else 'seller'
        notifications = notifications.filter(notification_type=f'for_{user_type}')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

