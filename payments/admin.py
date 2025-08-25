from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PaymentWebhook, RazorpayOrder
)


@admin.register(RazorpayOrder)
class RazorpayOrderAdmin(admin.ModelAdmin):
    """Admin for RazorpayOrder model."""
    
    list_display = ['razorpay_order_id', 'donation', 'amount', 'currency', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'currency', 'payment_method', 'created_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id', 'donation__campaign__title']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('donation', 'razorpay_order_id', 'amount', 'currency', 'status')
        }),
        ('Payment Details', {
            'fields': ('razorpay_payment_id', 'razorpay_signature', 'payment_method', 'bank', 'wallet')
        }),
        ('Error Handling', {
            'fields': ('error_code', 'error_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """Admin for PaymentWebhook model."""
    
    list_display = ['event_type', 'event_id', 'processed', 'received_at']
    list_filter = ['processed', 'event_type', 'received_at']
    search_fields = ['event_type', 'event_id']
    readonly_fields = ['event_type', 'event_id', 'payload', 'headers', 'received_at']
    ordering = ['-received_at']
    
    fieldsets = (
        ('Webhook Information', {
            'fields': ('event_type', 'event_id', 'processed')
        }),
        ('Webhook Data', {
            'fields': ('payload', 'headers'),
            'classes': ('collapse',)
        }),
        ('Processing', {
            'fields': ('processing_error', 'processed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('received_at',),
            'classes': ('collapse',)
        }),
    )




