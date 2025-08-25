from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class RazorpayOrder(models.Model):
    """Razorpay order model for tracking payment orders."""
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('attempted', 'Attempted'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donation = models.OneToOneField('donations.Donation', on_delete=models.CASCADE, related_name='razorpay_order')
    
    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    
    # Order details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    
    # Payment details
    payment_method = models.CharField(max_length=50, blank=True)  # card, netbanking, upi, etc.
    bank = models.CharField(max_length=100, blank=True)
    wallet = models.CharField(max_length=100, blank=True)
    
    # Error handling
    error_code = models.CharField(max_length=50, blank=True)
    error_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Razorpay Order')
        verbose_name_plural = _('Razorpay Orders')
        db_table = 'payments_razorpay_order'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.razorpay_order_id} - {self.amount} {self.currency}"
    
    @property
    def is_successful(self):
        """Check if payment was successful."""
        return self.status == 'paid'
    
    @property
    def is_failed(self):
        """Check if payment failed."""
        return self.status in ['failed', 'cancelled']


class PaymentWebhook(models.Model):
    """Payment webhook model for storing incoming webhook data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=100)
    event_id = models.CharField(max_length=255, unique=True)
    
    # Webhook data
    payload = models.JSONField()
    headers = models.JSONField(default=dict, blank=True)
    
    # Processing status
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    # Timestamps
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Payment Webhook')
        verbose_name_plural = _('Payment Webhooks')
        db_table = 'payments_payment_webhook'
        ordering = ['-received_at']
    
    def __str__(self):
        return f"Webhook {self.event_type} - {self.event_id}"


