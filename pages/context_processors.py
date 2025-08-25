from .models import SiteSettings, Statistics, Feature, Testimonial, FAQ, Banner


def cms_settings(request):
    """Add CMS settings and dynamic content to all templates."""
    
    # Initialize default values
    settings = None
    statistics = []
    features = []
    testimonials = []
    faqs = []
    banners = []
    
    # Try to get CMS data, but handle gracefully if tables don't exist
    try:
        # Get site settings
        settings = SiteSettings.get_settings()
    except Exception as e:
        print(f"Site settings not available: {e}")
    
    # Get active statistics for homepage
    try:
        statistics = Statistics.objects.filter(is_active=True, show_on_homepage=True).order_by('order')[:4]
    except Exception as e:
        print(f"Statistics not available: {e}")
    
    # Get active features for homepage
    try:
        features = Feature.objects.filter(is_active=True, show_on_homepage=True).order_by('order')[:6]
    except Exception as e:
        print(f"Features not available: {e}")
    
    # Get featured testimonials
    try:
        testimonials = Testimonial.objects.filter(is_active=True, is_featured=True).order_by('order')[:3]
    except Exception as e:
        print(f"Testimonials not available: {e}")
    
    # Get active FAQs
    try:
        faqs = FAQ.objects.filter(is_active=True).order_by('order')[:6]
    except Exception as e:
        print(f"FAQs not available: {e}")
    
    # Get active banners
    try:
        from django.utils import timezone
        now = timezone.now()
        banners = Banner.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-created_at')[:5]
    except Exception as e:
        print(f"Banners not available: {e}")
    
    return {
        'site_settings': settings,
        'homepage_statistics': statistics,
        'homepage_features': features,
        'featured_testimonials': testimonials,
        'homepage_faqs': faqs,
        'active_banners': banners,
    }
