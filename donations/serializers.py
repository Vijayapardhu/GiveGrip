from rest_framework import serializers
from .models import Campaign, Donation


class CampaignSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.get_full_name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['collected_amount', 'view_count', 'share_count', 'donor_count', 'created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        if obj.goal_amount > 0:
            return round((obj.collected_amount / obj.goal_amount) * 100, 1)
        return 0
    
    def get_days_remaining(self, obj):
        from django.utils import timezone
        if obj.end_date:
            remaining = obj.end_date - timezone.now().date()
            return max(0, remaining.days)
        return None


class DonationSerializer(serializers.ModelSerializer):
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    donor_name = serializers.CharField(source='donor.get_full_name', read_only=True)
    
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


