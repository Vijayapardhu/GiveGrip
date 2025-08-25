from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .models import Donation


@receiver(post_save, sender=Donation)
def update_campaign_amount(sender, instance, created, **kwargs):
    """Update campaign collected amount when a donation is paid"""
    if created and instance.status == 'paid':
        campaign = instance.campaign
        campaign.update_current_amount()
        campaign.save()


