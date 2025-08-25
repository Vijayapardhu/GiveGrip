from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from decimal import Decimal
import uuid

User = get_user_model()


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
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'))])
    collected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='INR')
    
    # Campaign creator
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    
    # Campaign category
    category = models.CharField(max_length=100, blank=True, help_text='Category of the campaign (e.g., Medical, Education, Emergency)')
    
    # Campaign settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Campaign dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Campaign content
    story = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='campaigns/covers/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    
    # Campaign statistics
    view_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    donor_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')
        db_table = 'donations_campaign'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('campaigns:campaign_detail', kwargs={'pk': self.pk})
    
    @property
    def progress_percentage(self):
        """Calculate campaign progress as percentage."""
        if self.goal_amount > 0:
            return min((self.collected_amount / self.goal_amount) * 100, 100)
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
        """Update the collected amount based on paid donations."""
        from django.db.models import Sum
        total_paid = self.donations.filter(status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0
        self.collected_amount = total_paid


class Donation(models.Model):
    """Donation model for tracking all donations."""
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    
    # Donation details
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    currency = models.CharField(max_length=3, default='INR')
    
    # Donation settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    is_anonymous = models.BooleanField(default=False)
    
    # Donor information
    donor_name = models.CharField(max_length=200, blank=True)  # For anonymous donations
    donor_message = models.TextField(blank=True)
    
    # Razorpay integration
    razorpay_order_id = models.CharField(max_length=255, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
        db_table = 'donations_donation'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Donation {self.id} - {self.amount} {self.currency}"
    
    def save(self, *args, **kwargs):
        # Set donor information for anonymous donations
        if self.is_anonymous and not self.donor_name:
            self.donor_name = "Anonymous Donor"
        
        super().save(*args, **kwargs)
        
        # Update campaign collected amount when donation is paid
        if self.status == 'paid':
            self.campaign.collected_amount += self.amount
            self.campaign.save(update_fields=['collected_amount'])
    
    @property
    def display_name(self):
        """Get display name based on anonymity setting."""
        if self.is_anonymous:
            return self.donor_name or "Anonymous Donor"
        return self.donor.display_name



