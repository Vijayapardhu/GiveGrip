from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PaymentMethod, PaymentTransaction, PaymentRefund, 
    PaymentWebhook, PaymentGatewayConfig
)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'payment_type', 'display_details', 
        'is_default', 'is_active', 'created_at'
    ]
    list_filter = ['payment_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'last_four', 'brand']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    def display_details(self, obj):
        """Display masked payment method details"""
        if obj.payment_type == 'card':
            return f"{obj.brand.title()} •••• {obj.last_four} (Exp: {obj.expiry_month}/{obj.expiry_year})"
        elif obj.payment_type == 'bank_account':
            return f"Bank Account •••• {obj.last_four}"
        return "N/A"
    
    display_details.short_description = "Payment Details"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'donation_link', 'donor', 'amount', 'currency', 
        'payment_gateway', 'status', 'created_at'
    ]
    list_filter = [
        'payment_gateway', 'status', 'currency', 'created_at'
    ]
    search_fields = [
        'transaction_id', 'donation__id', 'donation__donor__username',
        'donation__donor__email'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'gateway_response'
    ]
    list_per_page = 25
    
    def donation_link(self, obj):
        """Create a link to the donation"""
        if obj.donation:
            url = reverse('admin:donations_donation_change', args=[obj.donation.id])
            return format_html('<a href="{}">Donation #{}</a>', url, obj.donation.id)
        return "N/A"
    
    donation_link.short_description = "Donation"
    
    def donor(self, obj):
        """Display donor information"""
        if obj.donation and obj.donation.donor:
            return obj.donation.donor.username
        return "N/A"
    
    donor.short_description = "Donor"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'donation', 'donation__donor', 'payment_method'
        )


@admin.register(PaymentRefund)
class PaymentRefundAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'transaction_link', 'donor', 'amount', 'status', 
        'reason', 'processed_at', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'processed_at']
    search_fields = [
        'refund_id', 'transaction__transaction_id', 
        'transaction__donation__donor__username'
    ]
    readonly_fields = [
        'refund_id', 'created_at'
    ]
    list_per_page = 25
    
    def transaction_link(self, obj):
        """Create a link to the transaction"""
        if obj.transaction:
            url = reverse('admin:payments_paymenttransaction_change', args=[obj.transaction.id])
            return format_html('<a href="{}">Transaction #{}</a>', url, obj.transaction.id)
        return "N/A"
    
    transaction_link.short_description = "Transaction"
    
    def donor(self, obj):
        """Display donor information"""
        if obj.transaction and obj.transaction.donation and obj.transaction.donation.donor:
            return obj.transaction.donation.donor.username
        return "N/A"
    
    donor.short_description = "Donor"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'transaction', 'transaction__donation', 'transaction__donation__donor'
        )


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'gateway', 'event_type', 'processed', 'received_at'
    ]
    list_filter = ['gateway', 'processed', 'received_at']
    search_fields = ['gateway', 'event_type']
    readonly_fields = ['received_at', 'payload']
    list_per_page = 25
    
    def has_add_permission(self, request):
        """Webhooks are created automatically, not manually"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Webhooks should not be modified"""
        return False


@admin.register(PaymentGatewayConfig)
class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'gateway', 'is_active', 'test_mode', 
        'created_at', 'updated_at'
    ]
    list_filter = ['gateway', 'is_active', 'test_mode']
    search_fields = ['gateway']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('gateway', 'is_active', 'test_mode')
        }),
        ('API Credentials', {
            'fields': ('api_key', 'api_secret', 'webhook_secret'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('supported_currencies', 'supported_payment_methods', 'gateway_settings'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields read-only after creation"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ('gateway',)
        return self.readonly_fields




