from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Main router for campaigns
router = DefaultRouter()
router.register(r'categories', views.CampaignCategoryViewSet)
router.register(r'campaigns', views.CampaignViewSet)

urlpatterns = [
    # Main router URLs
    path('', include(router.urls)),
    
    # Simple nested URLs for now
    path('campaigns/<int:campaign_pk>/images/', views.CampaignImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='campaign-images'),
    path('campaigns/<int:campaign_pk>/updates/', views.CampaignUpdateViewSet.as_view({'get': 'list', 'post': 'create'}), name='campaign-updates'),
]



    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Campaign endpoints
    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<slug:slug>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<slug:slug>/update/', views.CampaignUpdateView.as_view(), name='campaign_update'),
    path('campaigns/<slug:slug>/stats/', views.campaign_stats, name='campaign_stats'),
    
    # Campaign updates
    path('campaigns/<slug:campaign_slug>/updates/', views.CampaignUpdateListView.as_view(), name='campaign_updates'),
    
    # Campaign comments
    path('campaigns/<slug:campaign_slug>/comments/', views.CampaignCommentListView.as_view(), name='campaign_comments'),
    
    # Campaign sharing
    path('campaigns/<slug:campaign_slug>/share/', views.CampaignShareView.as_view(), name='campaign_share'),
    
    # Featured campaigns
    path('campaigns/featured/', views.FeaturedCampaignsView.as_view(), name='featured_campaigns'),
    
    # Campaign search
    path('campaigns/search/', views.CampaignSearchView.as_view(), name='campaign_search'),
    
    # User progress for dashboard
    path('campaigns/user-progress/', views.user_campaign_progress, name='user_campaign_progress'),
]




app_name = 'campaigns'

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Campaign endpoints
    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<slug:slug>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<slug:slug>/update/', views.CampaignUpdateView.as_view(), name='campaign_update'),
    path('campaigns/<slug:slug>/stats/', views.campaign_stats, name='campaign_stats'),
    
    # Campaign updates
    path('campaigns/<slug:campaign_slug>/updates/', views.CampaignUpdateListView.as_view(), name='campaign_updates'),
    
    # Campaign comments
    path('campaigns/<slug:campaign_slug>/comments/', views.CampaignCommentListView.as_view(), name='campaign_comments'),
    
    # Campaign sharing
    path('campaigns/<slug:campaign_slug>/share/', views.CampaignShareView.as_view(), name='campaign_share'),
    
    # Featured campaigns
    path('campaigns/featured/', views.FeaturedCampaignsView.as_view(), name='featured_campaigns'),
    
    # Campaign search
    path('campaigns/search/', views.CampaignSearchView.as_view(), name='campaign_search'),
    
    # User progress for dashboard
    path('campaigns/user-progress/', views.user_campaign_progress, name='user_campaign_progress'),
]


