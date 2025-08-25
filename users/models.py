from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model for GiveGrip platform."""
    
    # Override username to make it optional
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    
    # Make email the primary identifier
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    
    # Additional profile fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # User preferences
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Social login fields
    google_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Meta
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users_user'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def is_donor(self):
        """Check if user has made any donations."""
        return hasattr(self, 'donations') and self.donations.exists()
    
    @property
    def is_campaign_creator(self):
        """Check if user has created any campaigns."""
        return hasattr(self, 'campaigns') and self.campaigns.exists()


class UserProfile(models.Model):
    """Extended user profile for additional information."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Professional information
    occupation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Social media
    twitter_handle = models.CharField(max_length=50, blank=True)
    linkedin_profile = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=50, blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_user_profile'
    
    def __str__(self):
        return f"Profile for {self.user.email}"


class PhoneVerification(models.Model):
    """Phone verification model for SMS verification."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_verifications')
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users_phone_verification'
    
    def __str__(self):
        return f"Verification for {self.phone_number}"
    
    @property
    def is_expired(self):
        """Check if verification code has expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at


