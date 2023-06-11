import random
import string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view
from account.models import UserProfile, SellerProfile, BuyerProfile
from account.serializers import UserSerializer
from django.conf import settings


@api_view(['POST'])
def seller_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        profile = UserProfile(user=user)
        profile.save()
        seller = SellerProfile(user_profile=profile)
        seller.save()

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
        profile = UserProfile(user=user)
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

