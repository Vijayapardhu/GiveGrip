from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, PhoneVerification

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone_number', 
            'profile_picture', 'bio', 'date_of_birth', 'address', 'city', 
            'state', 'country', 'postal_code', 'is_verified', 'email_verified', 
            'phone_verified', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number', 
            'password', 'password_confirm'
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone_number', 'profile_picture', 
            'bio', 'date_of_birth', 'address', 'city', 'state', 
            'country', 'postal_code'
        )


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class PhoneVerificationSerializer(serializers.ModelSerializer):
    """Serializer for PhoneVerification model."""
    
    class Meta:
        model = PhoneVerification
        fields = ('phone_number', 'verification_code')
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid phone number")
        return value


class PhoneVerificationRequestSerializer(serializers.Serializer):
    """Serializer for requesting phone verification."""
    
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        """Validate phone number format."""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid phone number")
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile information."""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone_number', 
            'profile_picture', 'bio', 'date_of_birth', 'address', 'city', 
            'state', 'country', 'postal_code', 'is_verified', 'email_verified', 
            'phone_verified', 'created_at', 'updated_at', 'profile'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


