from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PhoneVerification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model."""
    
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name', 'is_phone_verified', 'is_active', 'date_joined']
    list_filter = ['is_phone_verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'bio', 'date_of_birth')}),
        ('Social Media', {'fields': ('website', 'twitter', 'facebook', 'instagram', 'linkedin')}),
        ('Preferences', {'fields': ('newsletter_subscription', 'email_notifications', 'sms_notifications')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    """Admin for PhoneVerification model."""
    
    list_display = ['phone', 'otp', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
