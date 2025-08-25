from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
import uuid


class User(AbstractUser):
    """Custom User model with username and phone authentication."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=15, blank=True, null=True, help_text=_('Phone number for OTP authentication'))
    is_phone_verified = models.BooleanField(default=False, help_text=_('Whether phone number has been verified via OTP'))
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Social media
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'accounts_user'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.phone or 'No phone'})"
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def display_name(self):
        """Get display name for public view."""
        return self.full_name or self.username
    
    @classmethod
    def create_user(cls, username, email, password, **extra_fields):
        """Create a new user with the given username, email, and password."""
        if not username:
            raise ValueError('The username must be set')
        if not email:
            raise ValueError('The email must be set')
        
        email = cls.objects.normalize_email(email)
        user = cls(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class PhoneVerification(models.Model):
    """Phone verification model for OTP authentication."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)  # OTP code
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Phone Verification')
        verbose_name_plural = _('Phone Verifications')
        db_table = 'accounts_phone_verification'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Verification for {self.phone}"
