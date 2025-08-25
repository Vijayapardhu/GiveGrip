from django.contrib import admin
from .models import Campaign, Donation


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'goal_amount', 'collected_amount', 'status', 'is_featured', 'start_date', 'end_date', 'progress_percentage', 'days_remaining']
    list_filter = ['status', 'is_featured', 'category', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'creator__username', 'creator__email']
    readonly_fields = ['collected_amount', 'view_count', 'share_count', 'donor_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'story', 'creator', 'category')
        }),
        ('Financial', {
            'fields': ('goal_amount', 'collected_amount', 'currency')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'start_date', 'end_date')
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url')
        }),
        ('Statistics', {
            'fields': ('view_count', 'share_count', 'donor_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def progress_percentage(self, obj):
        if obj.goal_amount > 0:
            return f"{(obj.collected_amount / obj.goal_amount) * 100:.1f}%"
        return "0%"
    progress_percentage.short_description = 'Progress'
    
    def days_remaining(self, obj):
        from django.utils import timezone
        if obj.end_date:
            remaining = obj.end_date - timezone.now()
            return max(0, remaining.days)
        return "No end date"
    days_remaining.short_description = 'Days Remaining'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'donor', 'amount', 'currency', 'status', 'is_anonymous', 'created_at']
    list_filter = ['status', 'is_anonymous', 'currency', 'created_at']
    search_fields = ['campaign__title', 'donor__username', 'donor__email', 'donor_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Donation Details', {
            'fields': ('campaign', 'donor', 'amount', 'currency', 'status')
        }),
        ('Donor Information', {
            'fields': ('is_anonymous', 'donor_name', 'donor_message')
        }),
        ('Payment Details', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


