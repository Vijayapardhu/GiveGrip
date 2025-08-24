"""
URL configuration for Give Grip project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Frontend Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('faq/', views.faq, name='faq'),
    path('help-center/', views.help_center, name='help_center'),
    
    # New Enhanced Pages
    path('campaigns/', views.campaigns, name='campaigns'),
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('settings/', views.settings, name='settings'),
    path('donations/', views.donations, name='donations'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    # API Routes
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('campaigns.urls')),
    path('api/', include('donations.urls')),
    path('api/', include('payments.urls')),
    path('accounts/', include('allauth.urls')),

    # Contact form submission
    path('api/contact/', views.contact_submit, name='contact_submit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




