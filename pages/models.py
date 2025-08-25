from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid

User = get_user_model()


class SiteSettings(models.Model):
    """Global site settings for customization."""
    
    # Site Information
    site_name = models.CharField(max_length=100, default="GiveGrip")
    site_tagline = models.CharField(max_length=200, default="Make a Difference Through Crowdfunding")
    site_description = models.TextField(default="Empowering communities through crowdfunding. Make a difference in someone's life today.")
    
    # Contact Information
    contact_email = models.EmailField(default="support@givegrip.com")
    contact_phone = models.CharField(max_length=20, default="+1 (555) 123-4567")
    contact_address = models.TextField(default="123 Charity Way, Suite 100\nNew York, NY 10001")
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Business Hours
    business_hours = models.JSONField(default=dict, help_text="Business hours in JSON format")
    
    # Currency Settings
    currency_code = models.CharField(max_length=3, default="INR")
    currency_symbol = models.CharField(max_length=5, default="₹")
    currency_position = models.CharField(max_length=10, choices=[('before', 'Before'), ('after', 'After')], default="before")
    
    # Theme Settings
    primary_color = models.CharField(max_length=7, default="#2563eb")
    secondary_color = models.CharField(max_length=7, default="#059669")
    accent_color = models.CharField(max_length=7, default="#f59e0b")
    
    # SEO Settings
    meta_title = models.CharField(max_length=60, default="GiveGrip - Make a Difference Through Crowdfunding")
    meta_description = models.TextField(default="Join thousands of people helping others through crowdfunding. Every donation counts, every story matters.")
    meta_keywords = models.TextField(blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True)
    
    # Features Toggle
    enable_registration = models.BooleanField(default=True)
    enable_social_login = models.BooleanField(default=False)
    enable_newsletter = models.BooleanField(default=True)
    enable_live_chat = models.BooleanField(default=True)
    enable_testimonials = models.BooleanField(default=True)
    enable_faq = models.BooleanField(default=True)
    
    # Content Settings
    max_campaign_duration = models.PositiveIntegerField(default=90, help_text="Maximum campaign duration in days")
    min_donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    max_donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100000.00)
    
    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    
    # Security Settings
    enable_captcha = models.BooleanField(default=False)
    require_email_verification = models.BooleanField(default=True)
    require_phone_verification = models.BooleanField(default=False)
    
    # Maintenance Mode
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(default="We're currently performing maintenance. Please check back soon.")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class PageContent(models.Model):
    """Dynamic page content for CMS."""
    
    CONTENT_TYPES = [
        ('hero', 'Hero Section'),
        ('about', 'About Section'),
        ('features', 'Features Section'),
        ('testimonials', 'Testimonials Section'),
        ('faq', 'FAQ Section'),
        ('contact', 'Contact Section'),
        ('footer', 'Footer Section'),
        ('custom', 'Custom Section'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='custom')
    
    # Content
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='page_content/', blank=True, null=True)
    
    # Styling
    background_color = models.CharField(max_length=7, blank=True)
    text_color = models.CharField(max_length=7, blank=True)
    custom_css = models.TextField(blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Page Content')
        verbose_name_plural = _('Page Content')
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """Frequently Asked Questions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question


class Testimonial(models.Model):
    """Customer testimonials."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class Newsletter(models.Model):
    """Newsletter subscription."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Newsletter Subscription')
        verbose_name_plural = _('Newsletter Subscriptions')
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    """Contact form messages."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    newsletter_subscription = models.BooleanField(default=False, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class LegalDocument(models.Model):
    """Legal documents like Privacy Policy, Terms of Service."""
    
    DOCUMENT_TYPES = [
        ('privacy_policy', 'Privacy Policy'),
        ('terms_of_service', 'Terms of Service'),
        ('refund_policy', 'Refund Policy'),
        ('cookie_policy', 'Cookie Policy'),
        ('disclaimer', 'Disclaimer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    content = models.TextField()
    version = models.CharField(max_length=10, default="1.0")
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Legal Document')
        verbose_name_plural = _('Legal Documents')
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"{self.title} v{self.version}"


class Banner(models.Model):
    """Promotional banners and announcements."""
    
    BANNER_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('promotion', 'Promotion'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField()
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='info')
    is_active = models.BooleanField(default=True)
    show_on_all_pages = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Feature(models.Model):
    """Website features and capabilities."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='features/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class Statistics(models.Model):
    """Website statistics and metrics."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    value = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True, help_text="e.g., +, %, Cr")
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, default="#2563eb")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Statistic')
        verbose_name_plural = _('Statistics')
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.title}: {self.value}{self.suffix}"


class SocialProof(models.Model):
    """Social proof elements like logos, press mentions."""
    
    PROOF_TYPES = [
        ('logo', 'Company Logo'),
        ('press', 'Press Mention'),
        ('award', 'Award'),
        ('certification', 'Certification'),
        ('partnership', 'Partnership'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    proof_type = models.CharField(max_length=20, choices=PROOF_TYPES)
    image = models.ImageField(upload_to='social_proof/')
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Social Proof')
        verbose_name_plural = _('Social Proof')
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
