"""
URL configuration for GiveGrip project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),
    
    # App URLs
    path('', include('pages.urls')),
    path('campaigns/', include('donations.urls')),
    path('payment/', include('payments.urls')),
    path('user/', include('accounts.urls')),
    
    # Static and media files in development
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error pages
handler404 = 'givegrip.views.custom_404'
handler500 = 'givegrip.views.custom_500'




