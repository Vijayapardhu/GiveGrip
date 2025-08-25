from django.urls import path
from . import views

app_name = 'main_campaigns'

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('<uuid:pk>/', views.campaign_detail, name='campaign_detail'),
    path('<uuid:campaign_id>/donate/', views.donate, name='donate'),
    path('create/', views.create_campaign, name='create_campaign'),
    path('edit/<uuid:pk>/', views.edit_campaign, name='edit_campaign'),
]


