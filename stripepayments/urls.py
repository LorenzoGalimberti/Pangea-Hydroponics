from django.urls import path
from .views import CancelView,CreateCheckoutSessionView,SuccessView,stripe_webhook,cart_checkout
urlpatterns = [
    
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-checkout-session-cart/', cart_checkout, name='create-checkout-session-cart'),
    path('webhooks/stripe/',stripe_webhook,name='stripe-webhook'),
]
