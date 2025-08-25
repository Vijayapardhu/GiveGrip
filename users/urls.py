from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet, basename='profile')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('stats/', views.UserStatsView.as_view(), name='user-stats'),
]



    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Phone verification endpoints
    path('auth/send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('auth/verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    
    # Password reset endpoints
    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Google OAuth endpoint
    path('auth/google/', views.GoogleAuthView.as_view(), name='google_auth'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('donations/', views.user_donations, name='user_donations'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # Dashboard stats
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
]




app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Phone verification endpoints
    path('auth/send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('auth/verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    
    # Password reset endpoints
    path('auth/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Google OAuth endpoint
    path('auth/google/', views.GoogleAuthView.as_view(), name='google_auth'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('donations/', views.user_donations, name='user_donations'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # Dashboard stats
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
]


