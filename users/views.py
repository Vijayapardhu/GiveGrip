from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, UserProfile, PhoneVerification
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    PhoneVerificationSerializer, SendOTPSerializer, VerifyOTPSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    UserUpdateSerializer, ProfileUpdateSerializer
)


class UserRegistrationView(APIView):
    """User registration endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """User logout endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """User profile view and update."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile."""
        user_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        profile_serializer = ProfileUpdateSerializer(request.user.profile, data=request.data, partial=True)
        
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            
            updated_user = UserSerializer(request.user)
            return Response({
                'message': 'Profile updated successfully.',
                'user': updated_user.data
            })
        
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    """Send OTP to phone number."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            # Generate 6-digit OTP
            otp = ''.join(random.choices(string.digits, k=6))
            
            # Set expiration time (10 minutes)
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Save OTP
            PhoneVerification.objects.create(
                phone_number=phone_number,
                otp=otp,
                expires_at=expires_at
            )
            
            # TODO: Integrate with Twilio/Firebase to send SMS
            # For development, we'll just return the OTP
            if settings.DEBUG:
                return Response({
                    'message': 'OTP sent successfully.',
                    'otp': otp,  # Remove this in production
                    'phone_number': phone_number
                })
            
            return Response({
                'message': 'OTP sent successfully.',
                'phone_number': phone_number
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """Verify OTP and authenticate user."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            verification = serializer.validated_data['verification']
            phone_number = verification.phone_number
            
            # Mark OTP as verified
            verification.is_verified = True
            verification.save()
            
            # Check if user exists with this phone number
            try:
                user = User.objects.get(phone_number=phone_number)
                user.phone_verified = True
                user.save()
                
                # Login user
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Phone verified successfully.',
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
            
            except User.DoesNotExist:
                # Create new user with phone number
                user = User.objects.create_user(
                    username=f"user_{phone_number[-10:]}",
                    email=f"{phone_number}@temp.givegrip.com",
                    phone_number=phone_number,
                    phone_verified=True
                )
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
                # Login user
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Phone verified and account created successfully.',
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """Request password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # TODO: Send password reset email
            # For now, just return success message
            
            return Response({
                'message': 'Password reset email sent successfully.'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """Confirm password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Validate reset token and update password
            
            return Response({
                'message': 'Password reset successfully.'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    """Google OAuth authentication."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # TODO: Implement Google OAuth
        # This would typically handle the OAuth callback
        
        return Response({
            'message': 'Google authentication endpoint.'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_donations(request):
    """Get user's donation history."""
    donations = request.user.donations.all().order_by('-created_at')
    
    # TODO: Import and use donation serializer
    donation_data = []
    for donation in donations:
        donation_data.append({
            'id': donation.id,
            'amount': donation.amount,
            'campaign': donation.campaign.title,
            'created_at': donation.created_at,
            'status': donation.status
        })
    
    return Response({
        'donations': donation_data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user's donation statistics."""
    user = request.user
    
    # TODO: Calculate actual stats from donations
    stats = {
        'total_donations': 0,
        'total_amount': 0,
        'campaigns_supported': 0,
        'member_since': user.date_joined.strftime('%B %Y')
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get comprehensive dashboard statistics for the authenticated user."""
    user = request.user
    
    # Import necessary models
    from donations.models import Donation
    from campaigns.models import Campaign
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import datetime
    
    # Calculate total donations
    total_donations = Donation.objects.filter(
        donor=user, 
        status='completed'
    ).count()
    
    # Calculate total amount donated
    total_amount = Donation.objects.filter(
        donor=user, 
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate active campaigns supported
    active_campaigns = Campaign.objects.filter(
        donations__donor=user,
        donations__status='completed',
        status='active'
    ).distinct().count()
    
    # Calculate this month's donations
    current_month = timezone.now().month
    current_year = timezone.now().year
    this_month = Donation.objects.filter(
        donor=user,
        status='completed',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    stats = {
        'total_donations': total_donations,
        'total_amount': float(total_amount),
        'active_campaigns': active_campaigns,
        'this_month': float(this_month),
        'member_since': user.date_joined.strftime('%B %Y')
    }
    
    return Response(stats)



from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, UserProfile, PhoneVerification
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    PhoneVerificationSerializer, SendOTPSerializer, VerifyOTPSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    UserUpdateSerializer, ProfileUpdateSerializer
)


class UserRegistrationView(APIView):
    """User registration endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """User logout endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        logout(request)
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """User profile view and update."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile."""
        user_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        profile_serializer = ProfileUpdateSerializer(request.user.profile, data=request.data, partial=True)
        
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            
            updated_user = UserSerializer(request.user)
            return Response({
                'message': 'Profile updated successfully.',
                'user': updated_user.data
            })
        
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    """Send OTP to phone number."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            # Generate 6-digit OTP
            otp = ''.join(random.choices(string.digits, k=6))
            
            # Set expiration time (10 minutes)
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Save OTP
            PhoneVerification.objects.create(
                phone_number=phone_number,
                otp=otp,
                expires_at=expires_at
            )
            
            # TODO: Integrate with Twilio/Firebase to send SMS
            # For development, we'll just return the OTP
            if settings.DEBUG:
                return Response({
                    'message': 'OTP sent successfully.',
                    'otp': otp,  # Remove this in production
                    'phone_number': phone_number
                })
            
            return Response({
                'message': 'OTP sent successfully.',
                'phone_number': phone_number
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """Verify OTP and authenticate user."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            verification = serializer.validated_data['verification']
            phone_number = verification.phone_number
            
            # Mark OTP as verified
            verification.is_verified = True
            verification.save()
            
            # Check if user exists with this phone number
            try:
                user = User.objects.get(phone_number=phone_number)
                user.phone_verified = True
                user.save()
                
                # Login user
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Phone verified successfully.',
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
            
            except User.DoesNotExist:
                # Create new user with phone number
                user = User.objects.create_user(
                    username=f"user_{phone_number[-10:]}",
                    email=f"{phone_number}@temp.givegrip.com",
                    phone_number=phone_number,
                    phone_verified=True
                )
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
                # Login user
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'message': 'Phone verified and account created successfully.',
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """Request password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # TODO: Send password reset email
            # For now, just return success message
            
            return Response({
                'message': 'Password reset email sent successfully.'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """Confirm password reset."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Validate reset token and update password
            
            return Response({
                'message': 'Password reset successfully.'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    """Google OAuth authentication."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        # TODO: Implement Google OAuth
        # This would typically handle the OAuth callback
        
        return Response({
            'message': 'Google authentication endpoint.'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_donations(request):
    """Get user's donation history."""
    donations = request.user.donations.all().order_by('-created_at')
    
    # TODO: Import and use donation serializer
    donation_data = []
    for donation in donations:
        donation_data.append({
            'id': donation.id,
            'amount': donation.amount,
            'campaign': donation.campaign.title,
            'created_at': donation.created_at,
            'status': donation.status
        })
    
    return Response({
        'donations': donation_data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user's donation statistics."""
    user = request.user
    
    # TODO: Calculate actual stats from donations
    stats = {
        'total_donations': 0,
        'total_amount': 0,
        'campaigns_supported': 0,
        'member_since': user.date_joined.strftime('%B %Y')
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """Get comprehensive dashboard statistics for the authenticated user."""
    user = request.user
    
    # Import necessary models
    from donations.models import Donation
    from campaigns.models import Campaign
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import datetime
    
    # Calculate total donations
    total_donations = Donation.objects.filter(
        donor=user, 
        status='completed'
    ).count()
    
    # Calculate total amount donated
    total_amount = Donation.objects.filter(
        donor=user, 
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate active campaigns supported
    active_campaigns = Campaign.objects.filter(
        donations__donor=user,
        donations__status='completed',
        status='active'
    ).distinct().count()
    
    # Calculate this month's donations
    current_month = timezone.now().month
    current_year = timezone.now().year
    this_month = Donation.objects.filter(
        donor=user,
        status='completed',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    stats = {
        'total_donations': total_donations,
        'total_amount': float(total_amount),
        'active_campaigns': active_campaigns,
        'this_month': float(this_month),
        'member_since': user.date_joined.strftime('%B %Y')
    }
    
    return Response(stats)


