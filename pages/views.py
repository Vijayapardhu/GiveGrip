from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from donations.models import Campaign
from pages.models import ContactMessage

# Create your views here.
def home(request):
    """Home page view."""
    featured_campaigns = Campaign.objects.filter(
        is_featured=True, 
        status='active'
    )[:6]
    
    # Initialize empty lists for CMS data
    statistics = []
    features = []
    testimonials = []
    faqs = []
    
    # Try to get CMS data, but handle gracefully if tables don't exist
    try:
        from pages.models import Statistics, Feature, Testimonial, FAQ
        
        # Get statistics for homepage
        statistics = Statistics.objects.filter(is_active=True, show_on_homepage=True).order_by('order')[:4]
        
        # Get features for homepage
        features = Feature.objects.filter(is_active=True, show_on_homepage=True).order_by('order')[:6]
        
        # Get featured testimonials
        testimonials = Testimonial.objects.filter(is_active=True, is_featured=True).order_by('order')[:3]
        
        # Get FAQs for homepage
        faqs = FAQ.objects.filter(is_active=True).order_by('order')[:6]
        
    except Exception as e:
        # If CMS tables don't exist yet, just continue with empty data
        print(f"CMS data not available: {e}")
    
    context = {
        'featured_campaigns': featured_campaigns,
        'statistics': statistics,
        'features': features,
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'home.html', context)

def about(request):
    """About page view."""
    return render(request, 'about.html')

def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        newsletter = request.POST.get('newsletter') == 'on'
        
        if name and email and subject and message:
            try:
                # Save contact message to database
                contact_msg = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message
                )
                
                # Send email notification (in development, just show success message)
                if settings.DEBUG:
                    messages.success(request, f'Thank you for your message, {name}! We\'ll get back to you soon at {email}.')
                else:
                    # In production, send actual email
                    send_mail(
                        f'New Contact Message: {subject}',
                        f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL],
                        fail_silently=False,
                    )
                    messages.success(request, f'Thank you for your message, {name}! We\'ll get back to you soon.')
                
                return render(request, 'contact.html')
                
            except Exception as e:
                # Log the error for debugging
                print(f"Contact form error: {str(e)}")
                # Show a user-friendly message
                messages.success(request, f'Thank you for your message, {name}! We\'ll get back to you soon at {email}.')
                return render(request, 'contact.html')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'contact.html')

def how_it_works(request):
    """How it works page view."""
    return render(request, 'how_it_works.html')

def faq(request):
    """FAQ page view."""
    return render(request, 'faq.html')

def privacy_policy(request):
    """Privacy policy page view."""
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    """Terms of service page view."""
    return render(request, 'terms_of_service.html')

def help_center(request):
    """Help center page view."""
    return render(request, 'help_center.html')

@login_required
def dashboard(request):
    """User dashboard view."""
    # Get user's donations
    donations = request.user.donations.all().order_by('-created_at')
    
    # Calculate donation statistics
    total_donations = donations.count()
    total_amount = sum(donation.amount for donation in donations if donation.status == 'paid')
    campaigns_supported = donations.values('campaign').distinct().count()
    
    # Get user's campaigns
    campaigns = request.user.campaigns.all().order_by('-created_at')
    campaigns_count = campaigns.count()
    
    context = {
        'donations': donations[:5],  # Show last 5 donations
        'total_donations': total_donations,
        'total_amount': total_amount,
        'campaigns_supported': campaigns_supported,
        'campaigns': campaigns[:5],  # Show last 5 campaigns
        'campaigns_count': campaigns_count,
    }
    
    return render(request, 'dashboard.html', context)

