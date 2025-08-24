from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'donations'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'donations', views.DonationViewSet, basename='donation')
router.register(r'goals', views.DonationGoalViewSet, basename='donation_goal')
router.register(r'milestones', views.DonationMilestoneViewSet, basename='donation_milestone')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Search and analytics
    path('donations/search/', views.donation_search, name='donation_search'),
    path('donations/stats/', views.donation_stats, name='donation_stats'),
    path('campaigns/<int:campaign_id>/donation-stats/', views.campaign_donation_stats, name='campaign_donation_stats'),
    path('donations/analytics/', views.donation_analytics, name='donation_analytics'),
    
    # Recent donations for dashboard
    path('donations/recent/', views.recent_donations, name='recent_donations'),
]



from . import views

app_name = 'donations'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'donations', views.DonationViewSet, basename='donation')
router.register(r'goals', views.DonationGoalViewSet, basename='donation_goal')
router.register(r'milestones', views.DonationMilestoneViewSet, basename='donation_milestone')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Search and analytics
    path('donations/search/', views.donation_search, name='donation_search'),
    path('donations/stats/', views.donation_stats, name='donation_stats'),
    path('campaigns/<int:campaign_id>/donation-stats/', views.campaign_donation_stats, name='campaign_donation_stats'),
    path('donations/analytics/', views.donation_analytics, name='donation_analytics'),
    
    # Recent donations for dashboard
    path('donations/recent/', views.recent_donations, name='recent_donations'),
]


