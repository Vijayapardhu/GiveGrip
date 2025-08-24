from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def about(request):
    """About page view"""
    return render(request, 'about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')


@login_required
def dashboard(request):
    """User dashboard view"""
    return render(request, 'dashboard.html')


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'profile.html')


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'terms_of_service.html')


def faq(request):
    """FAQ page"""
    return render(request, 'faq.html')


def help_center(request):
    """Help center page"""
    return render(request, 'help_center.html')


def campaigns(request):
    """Campaigns listing page view"""
    return render(request, 'campaigns.html')


@login_required
def create_campaign(request):
    """Create campaign page view"""
    return render(request, 'create_campaign.html')


def how_it_works(request):
    """How it works page view"""
    return render(request, 'how_it_works.html')


def success_stories(request):
    """Success stories page view"""
    return render(request, 'success_stories.html')


def cookie_policy(request):
    """Cookie policy page view"""
    return render(request, 'cookie_policy.html')


def accessibility(request):
    """Accessibility page view"""
    return render(request, 'accessibility.html')


def sitemap(request):
    """Sitemap page view"""
    return render(request, 'sitemap.html')


@login_required
def settings(request):
    """User settings page view"""
    return render(request, 'settings.html')


@login_required
def donations(request):
    """User donations page view"""
    return render(request, 'donations.html')


def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')


def register(request):
    """Register page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'register.html')


def logout_view(request):
    """Logout view"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


@csrf_exempt
def contact_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            email = data.get('email', '')
            message = data.get('message', '')
            
            # Here you would typically save to database and send email
            # For now, just return success
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We\'ll get back to you soon.'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid data format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed.'
    }, status=405)




