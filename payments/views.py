"""
Views for the payments application.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from .models import RazorpayOrder, PaymentWebhook

@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """Handle Razorpay webhook notifications."""
    try:
        # Get webhook data
        webhook_data = json.loads(request.body)
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        
        # Verify webhook signature (in production, use proper secret)
        # For now, just process the webhook
        event_type = webhook_data.get('event')
        
        if event_type == 'payment.captured':
            # Payment was successful
            payment_data = webhook_data.get('payload', {}).get('payment', {})
            order_id = payment_data.get('order_id')
            
            try:
                razorpay_order = RazorpayOrder.objects.get(razorpay_order_id=order_id)
                razorpay_order.status = 'paid'
                razorpay_order.razorpay_payment_id = payment_data.get('id')
                razorpay_order.save()
                
                # Update donation status
                donation = razorpay_order.donation
                donation.status = 'paid'
                donation.razorpay_payment_id = payment_data.get('id')
                donation.save()
                
            except RazorpayOrder.DoesNotExist:
                pass
                
        elif event_type == 'payment.failed':
            # Payment failed
            payment_data = webhook_data.get('payload', {}).get('payment', {})
            order_id = payment_data.get('order_id')
            
            try:
                razorpay_order = RazorpayOrder.objects.get(razorpay_order_id=order_id)
                razorpay_order.status = 'failed'
                razorpay_order.error_code = payment_data.get('error_code')
                razorpay_order.error_description = payment_data.get('error_description')
                razorpay_order.save()
                
                # Update donation status
                donation = razorpay_order.donation
                donation.status = 'failed'
                donation.save()
                
            except RazorpayOrder.DoesNotExist:
                pass
        
        return HttpResponse(status=200)
        
    except Exception as e:
        return HttpResponse(status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def payment_success(request):
    """Payment success page."""
    if request.method == 'POST':
        try:
            # Handle payment verification
            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')
            donation_id = data.get('donation_id')
            
            # Verify payment signature (in production, use proper verification)
            # For now, just update the donation status
            
            from donations.models import Donation
            from .models import RazorpayOrder
            
            try:
                donation = Donation.objects.get(id=donation_id)
                donation.status = 'paid'
                donation.razorpay_payment_id = razorpay_payment_id
                donation.save()
                
                # Update campaign statistics
                campaign = donation.campaign
                campaign.update_current_amount()
                campaign.save()
                
                # Update order status
                try:
                    order = RazorpayOrder.objects.get(razorpay_order_id=razorpay_order_id)
                    order.status = 'paid'
                    order.razorpay_payment_id = razorpay_payment_id
                    order.save()
                except RazorpayOrder.DoesNotExist:
                    pass
                
                return JsonResponse({'success': True})
                
            except Donation.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Donation not found'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'payment_success.html')

def payment_failure(request):
    """Payment failure page."""
    return render(request, 'payment_failure.html')

