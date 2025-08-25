from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, PhoneVerification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model."""
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('is_staff', 'is_active', 'is_verified', 'email_verified', 'phone_verified', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'phone_number', 'profile_picture', 
                'bio', 'date_of_birth', 'address', 'city', 'state', 
                'country', 'postal_code'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 
                'user_permissions', 'is_verified', 'email_verified', 'phone_verified'
            ),
        }),
        (_('Social login'), {
            'fields': ('google_id', 'facebook_id'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    
    list_display = ('user', 'occupation', 'company', 'newsletter_subscription')
    list_filter = ('newsletter_subscription', 'email_notifications', 'sms_notifications')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'occupation')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    """Admin for PhoneVerification model."""
    
    list_display = ('user', 'phone_number', 'is_verified', 'expires_at', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__email', 'phone_number')
    readonly_fields = ('created_at',)
