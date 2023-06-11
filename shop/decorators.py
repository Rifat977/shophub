from functools import wraps
from django.http import HttpResponseForbidden
from account.models import SellerProfile, BuyerProfile

def seller_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user = self.request.user
        try:
            seller_profile = SellerProfile.objects.get(user_profile__user=user)
        except SellerProfile.DoesNotExist:
            return HttpResponseForbidden("You must be a seller to access this page.")
        return view_func(self, request, *args, **kwargs)
    return wrapper

def buyer_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        user = self.request.user
        try:
            buyer_profile = BuyerProfile.objects.get(user_profile__user=user)
        except BuyerProfile.DoesNotExist:
            return HttpResponseForbidden("You must be a buyer to access this page.")
        return view_func(self, request, *args, **kwargs)
    return wrapper
