from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save)
def update_campaign_on_payment(sender, instance, created, **kwargs):
    """Update campaign collected amount when payment is successful."""
    # Check if this is a RazorpayOrder
    if sender._meta.app_label == 'payments' and sender._meta.model_name == 'razorpayorder':
        if created and instance.status == 'paid':
            try:
                # Update campaign collected amount
                campaign = instance.donation.campaign
                campaign.update_current_amount()
                campaign.save()
            except Exception as e:
                # Log the error but don't break the signal
                print(f"Error updating campaign: {e}")


@receiver(post_save)
def process_webhook(sender, instance, created, **kwargs):
    """Process webhook data when received."""
    # Check if this is a PaymentWebhook
    if sender._meta.app_label == 'payments' and sender._meta.model_name == 'paymentwebhook':
        if created:
            # Process webhook data here
            pass