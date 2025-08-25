from django.urls import path
from . import views

app_name = 'main_payment'

urlpatterns = [
    path('webhook/razorpay/', views.razorpay_webhook, name='razorpay_webhook'),
    path('success/', views.payment_success, name='payment_success'),
    path('failure/', views.payment_failure, name='payment_failure'),
]


