from rest_framework import serializers
from .models import RazorpayOrder, PaymentWebhook


class RazorpayOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RazorpayOrder
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWebhook
        fields = '__all__'
        read_only_fields = ['created_at']


