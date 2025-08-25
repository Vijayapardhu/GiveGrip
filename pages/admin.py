from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    SiteSettings, PageContent, FAQ, Testimonial, Newsletter, 
    ContactMessage, LegalDocument, Banner, Feature, Statistics, SocialProof
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin interface for site settings."""
    
    def has_add_permission(self, request):
        # Only allow one site settings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of site settings
        return False
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Business Hours', {
            'fields': ('business_hours',),
            'classes': ('collapse',)
        }),
        ('Currency Settings', {
            'fields': ('currency_code', 'currency_symbol', 'currency_position')
        }),
        ('Theme Settings', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id'),
            'classes': ('collapse',)
        }),
        ('Features Toggle', {
            'fields': ('enable_registration', 'enable_social_login', 'enable_newsletter', 
                      'enable_testimonials', 'enable_faq'),
            'classes': ('collapse',)
        }),
        ('Content Settings', {
            'fields': ('max_campaign_duration', 'min_donation_amount', 'max_donation_amount'),
            'classes': ('collapse',)
        }),
        ('Notification Settings', {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications'),
            'classes': ('collapse',)
        }),
        ('Security Settings', {
            'fields': ('enable_captcha', 'require_email_verification', 'require_phone_verification'),
            'classes': ('collapse',)
        }),
        ('Maintenance Mode', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    """Admin interface for page content."""
    
    list_display = ('title', 'content_type', 'is_active', 'show_on_homepage', 'order', 'created_at')
    list_filter = ('content_type', 'is_active', 'show_on_homepage', 'created_at')
    search_fields = ('title', 'heading', 'content')
    list_editable = ('is_active', 'show_on_homepage', 'order')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content_type')
        }),
        ('Content', {
            'fields': ('heading', 'subheading', 'content', 'image')
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color', 'custom_css'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order', 'show_on_homepage')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin interface for FAQs."""
    
    list_display = ('question', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'category')
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        ('FAQ Information', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for testimonials."""
    
    list_display = ('name', 'role', 'company', 'rating', 'is_featured', 'is_active', 'order')
    list_filter = ('rating', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'role', 'company', 'content')
    list_editable = ('rating', 'is_featured', 'is_active', 'order')
    
    fieldsets = (
        ('Person Information', {
            'fields': ('name', 'role', 'company', 'avatar')
        }),
        ('Testimonial Content', {
            'fields': ('content', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin interface for newsletter subscriptions."""
    
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_editable = ('is_active',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    
    actions = ['export_emails']
    
    def export_emails(self, request, queryset):
        """Export emails to CSV."""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_emails.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'First Name', 'Last Name', 'Subscribed At'])
        
        for subscription in queryset:
            writer.writerow([
                subscription.email,
                subscription.first_name,
                subscription.last_name,
                subscription.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    export_emails.short_description = "Export selected emails to CSV"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for contact messages."""
    
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'newsletter_subscription', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('status',)
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Settings', {
            'fields': ('status', 'newsletter_subscription')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_closed']
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "Mark selected messages as closed"


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    """Admin interface for legal documents."""
    
    list_display = ('title', 'document_type', 'version', 'is_active', 'effective_date')
    list_filter = ('document_type', 'is_active', 'effective_date')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'document_type', 'version', 'effective_date')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Admin interface for banners."""
    
    list_display = ('title', 'banner_type', 'is_active', 'show_on_all_pages', 'show_on_homepage', 'start_date', 'end_date')
    list_filter = ('banner_type', 'is_active', 'show_on_all_pages', 'show_on_homepage', 'start_date', 'end_date')
    search_fields = ('title', 'message')
    list_editable = ('is_active', 'show_on_all_pages', 'show_on_homepage')
    
    fieldsets = (
        ('Banner Information', {
            'fields': ('title', 'message', 'banner_type')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'show_on_all_pages', 'show_on_homepage')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """Admin interface for features."""
    
    list_display = ('title', 'icon', 'is_active', 'order', 'show_on_homepage')
    list_filter = ('is_active', 'show_on_homepage', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order', 'show_on_homepage')
    
    fieldsets = (
        ('Feature Information', {
            'fields': ('title', 'description', 'icon', 'image')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'show_on_homepage')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    """Admin interface for statistics."""
    
    list_display = ('title', 'value', 'suffix', 'icon', 'color', 'is_active', 'order', 'show_on_homepage')
    list_filter = ('is_active', 'show_on_homepage', 'created_at')
    search_fields = ('title', 'value')
    list_editable = ('value', 'suffix', 'color', 'is_active', 'order', 'show_on_homepage')
    
    fieldsets = (
        ('Statistic Information', {
            'fields': ('title', 'value', 'suffix', 'icon', 'color')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'show_on_homepage')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SocialProof)
class SocialProofAdmin(admin.ModelAdmin):
    """Admin interface for social proof."""
    
    list_display = ('title', 'proof_type', 'is_active', 'order', 'show_on_homepage')
    list_filter = ('proof_type', 'is_active', 'show_on_homepage', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order', 'show_on_homepage')
    
    fieldsets = (
        ('Social Proof Information', {
            'fields': ('title', 'proof_type', 'image', 'url', 'description')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'show_on_homepage')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


# Customize admin site
admin.site.site_header = "GiveGrip CMS Administration"
admin.site.site_title = "GiveGrip CMS"
admin.site.index_title = "Welcome to GiveGrip CMS"
