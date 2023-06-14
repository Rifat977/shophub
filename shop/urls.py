from django.urls import path
from shop.views import *

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', Products.as_view(), name='product-list'),
    path('product/<int:id>/', ProductRetrieveAPIView.as_view(), name='product-retrieve'), #get request
    path('product/', ProductCreateAPIView.as_view(), name='product-list'),
    path('edit/product/<int:pk>/', ProductUD.as_view(), name='product-detail'), # put, delete request

    path('orders/', InvoiceListAPIView.as_view(), name='invoice-list'),
    path('orders/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice-detail'),

    path('change-mode/', ChangeToBuyerModeAPIView.as_view(), name='change-mode'),
    path('followers/', SellerFollowersAPIView.as_view(), name='followers'),

    path('invitations/', InvitationListAPIView.as_view(), name='invitation-list'), # invitations send list
    path('invitations/<int:pk>/', InvitationDetailAPIView.as_view(), name='invitation-detail'), # single invitation
    path('invitations/send/', InvitationSendAPIView.as_view(), name='invitation-send'), # send invitation
    path('invitations/sends/accepted/', AcceptedInvitationsSenderAPIView.as_view(), name='accepted-list-sends'),

    # Accepted receiver
    path('invitations/received/accepted/', AcceptedInvitationsReceiverAPIView.as_view(), name='accepted-list-receiveds'),
    path('invitations/accept/', InvitationAcceptAPIView.as_view(), name='invitation-send'),
    
    path('product/<int:product_id>/reviews/', ProductReviewListAPIView.as_view(), name='product-reviews'),


]
