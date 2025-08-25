from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from decimal import Decimal
import uuid

User = get_user_model()


class CampaignCategory(models.Model):
    """Campaign category model for organizing campaigns."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    is_active = models.BooleanField(default=True)
    
    # SEO fields
    slug = models.SlugField(max_length=100, unique=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Campaign Category')
        verbose_name_plural = _('Campaign Categories')
        db_table = 'campaigns_campaign_category'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('campaigns:category_detail', kwargs={'slug': self.slug})


class Campaign(models.Model):
    """Campaign model for fundraising campaigns."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    category = models.ForeignKey(CampaignCategory, on_delete=models.PROTECT, related_name='campaigns')
    
    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Campaign details
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))])
    currency = models.CharField(max_length=3, default='USD')
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Campaign settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Campaign dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Campaign content
    story = models.TextField(blank=True)
    impact_statement = models.TextField(blank=True)
    beneficiary_info = models.TextField(blank=True)
    
    # Media
    cover_image = models.ImageField(upload_to='campaigns/covers/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Campaign statistics
    view_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    donor_count = models.PositiveIntegerField(default=0)
    
    # Moderation
    rejection_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_campaigns')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        db_table = 'campaigns_campaign'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['goal_amount']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('campaigns:campaign_detail', kwargs={'slug': self.slug})
    
    @property
    def progress_percentage(self):
        """Calculate campaign progress as percentage."""
        if self.goal_amount > 0:
            return min((self.current_amount / self.goal_amount) * 100, 100)
        return 0
    
    @property
    def days_remaining(self):
        """Calculate days remaining in campaign."""
        from django.utils import timezone
        now = timezone.now()
        if now < self.end_date:
            return (self.end_date - now).days
        return 0
    
    @property
    def is_active_campaign(self):
        """Check if campaign is currently active."""
        from django.utils import timezone
        now = timezone.now()
        return (self.status == 'active' and 
                self.start_date <= now <= self.end_date)
    
    def update_current_amount(self):
        """Update current amount based on donations."""
        # Use a lazy import to avoid circular dependency
        from django.apps import apps
        Donation = apps.get_model('donations', 'Donation')
        
        total_donations = Donation.objects.filter(
            campaign=self, 
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        self.current_amount = total_donations
        self.save(update_fields=['current_amount'])


class CampaignImage(models.Model):
    """Campaign image model for additional campaign images."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='campaigns/images/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Campaign Image')
        verbose_name_plural = _('Campaign Images')
        db_table = 'campaigns_campaign_image'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image for {self.campaign.title}"


class CampaignUpdate(models.Model):
    """Campaign update model for campaign progress updates."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Media
    image = models.ImageField(upload_to='campaigns/updates/', blank=True, null=True)
    
    # Visibility
    is_public = models.BooleanField(default=True)
    notify_donors = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Campaign Update')
        verbose_name_plural = _('Campaign Updates')
        db_table = 'campaigns_campaign_update'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Update: {self.title} - {self.campaign.title}"


