from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from .models import User, PhoneVerification
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.http import urlsafe_base64_decode

def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('pages:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember') == 'on'
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Handle remember me functionality
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('pages:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('pages:home')
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        
        if not password1:
            errors.append('Password is required.')
        elif len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if not first_name:
            errors.append('First name is required.')
        
        if not last_name:
            errors.append('Last name is required.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone
                )
                
                # Log user in with the default backend
                from django.contrib.auth import authenticate
                user = authenticate(request, username=username, password=password1)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'Account created successfully!')
                    return redirect('pages:home')
                else:
                    messages.error(request, 'Account created but login failed. Please login manually.')
                    return redirect('accounts:login')
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'register.html')

@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('pages:home')

@login_required
def profile_view(request):
    """User profile view."""
    # Get user's donations
    donations = request.user.donations.all().order_by('-created_at')
    
    # Calculate donation statistics
    total_donations = donations.count()
    total_amount = sum(donation.amount for donation in donations if donation.status == 'paid')
    campaigns_supported = donations.values('campaign').distinct().count()
    
    # Get user's campaigns
    campaigns = request.user.campaigns.all().order_by('-created_at')
    
    context = {
        'donations': donations[:5],  # Show last 5 donations
        'total_donations': total_donations,
        'total_amount': total_amount,
        'campaigns_supported': campaigns_supported,
        'campaigns': campaigns[:5],  # Show last 5 campaigns
        'campaigns_count': campaigns.count(),
    }
    
    return render(request, 'profile.html', context)

def forgot_password(request):
    """Forgot password view."""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email)
                
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create reset URL
                reset_url = request.build_absolute_uri(
                    reverse('accounts:reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Send email (in development, just show the link)
                if settings.DEBUG:
                    messages.success(request, f'Password reset link: {reset_url}')
                else:
                    # In production, send actual email
                    subject = 'Password Reset - GiveGrip'
                    message = f'Click the following link to reset your password: {reset_url}'
                    send_mail(subject, message, 'noreply@givegrip.com', [email])
                    messages.success(request, 'Password reset email sent successfully!')
                
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
        else:
            messages.error(request, 'Please enter your email address.')
    
    return render(request, 'forgot_password.html')

def reset_password_confirm(request, uidb64, token):
    """Reset password confirmation view."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2:
                if password1 == password2:
                    if len(password1) >= 8:
                        user.set_password(password1)
                        user.save()
                        messages.success(request, 'Password reset successfully! Please login with your new password.')
                        return redirect('accounts:login')
                    else:
                        messages.error(request, 'Password must be at least 8 characters long.')
                else:
                    messages.error(request, 'Passwords do not match.')
            else:
                messages.error(request, 'Please fill in all fields.')
        
        return render(request, 'reset_password_confirm.html')
    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('accounts:login')

def otp_start(request):
    """Start OTP verification process."""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        # In development, use a fake OTP
        otp = '123456'
        
        # Create or update phone verification
        verification, created = PhoneVerification.objects.get_or_create(
            phone=phone,
            defaults={'otp': otp}
        )
        if not created:
            verification.otp = otp
            verification.save()
        
        messages.success(request, f'OTP sent to {phone}. Use 123456 for testing.')
        return redirect('accounts:otp_verify')
    
    return render(request, 'otp_start.html')

def otp_verify(request):
    """Verify OTP code."""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        
        try:
            verification = PhoneVerification.objects.get(phone=phone, otp=otp)
            verification.is_verified = True
            verification.save()
            
            messages.success(request, 'Phone number verified successfully!')
            return redirect('accounts:login')
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP code.')
    
    return render(request, 'otp_verify.html')

@login_required
def my_donations(request):
    """View user's donations."""
    donations = request.user.donations.all().order_by('-created_at')
    return render(request, 'my_donations.html', {'donations': donations})
