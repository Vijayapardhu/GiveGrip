from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Campaign, Donation

def campaign_list(request):
    """List all active campaigns."""
    campaigns = Campaign.objects.filter(status='active').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(campaigns, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'campaigns': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'campaign_list.html', context)

def campaign_detail(request, pk):
    """Show campaign details."""
    campaign = get_object_or_404(Campaign, pk=pk)
    
    # Get recent donations
    recent_donations = campaign.donations.filter(status='paid').order_by('-created_at')[:5]
    
    context = {
        'campaign': campaign,
        'recent_donations': recent_donations,
    }
    return render(request, 'campaign_detail.html', context)

@login_required
def donate(request, campaign_id):
    """Donate to a campaign."""
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        if amount and float(amount) > 0:
            try:
                # Create donation with pending status
                donation = Donation.objects.create(
                    campaign=campaign,
                    donor=request.user,
                    amount=amount,
                    donor_message=message,
                    is_anonymous=is_anonymous,
                    currency=campaign.currency,
                    status='pending'
                )
                
                # Create test order for development
                import uuid
                
                # Generate test order ID
                test_order_id = f"order_test_{uuid.uuid4().hex[:16]}"
                
                # Save order to database
                from payments.models import RazorpayOrder
                order_record = RazorpayOrder.objects.create(
                    donation=donation,
                    razorpay_order_id=test_order_id,
                    amount=amount,
                    currency=campaign.currency,
                    status='created'
                )
                
                # Redirect to payment gateway
                context = {
                    'order_id': test_order_id,
                    'amount': int(float(amount) * 100),  # Convert to paise for display
                    'currency': campaign.currency,
                    'key_id': 'test_key',  # Placeholder for testing
                    'donation': donation,
                    'campaign': campaign
                }
                
                return render(request, 'payment_gateway.html', context)
                
            except Exception as e:
                messages.error(request, f'Error processing donation: {str(e)}')
        else:
            messages.error(request, 'Please enter a valid amount.')
    
    context = {
        'campaign': campaign,
    }
    return render(request, 'donate.html', context)

@login_required
def create_campaign(request):
    """Create a new campaign."""
    if request.method == 'POST':
        # Handle campaign creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        goal_amount = request.POST.get('goal_amount')
        story = request.POST.get('story', '')
        currency = request.POST.get('currency', 'USD')
        category = request.POST.get('category', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if title and description and goal_amount:
            try:
                from django.utils import timezone
                from datetime import timedelta
                
                # Set default dates if not provided
                if not start_date:
                    start_date = timezone.now()
                else:
                    try:
                        # Parse date string to datetime
                        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
                        start_date = timezone.make_aware(start_date)
                    except ValueError:
                        start_date = timezone.now()
                
                if not end_date:
                    end_date = start_date + timedelta(days=30)  # Default 30 days
                else:
                    try:
                        # Parse date string to datetime
                        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
                        end_date = timezone.make_aware(end_date)
                    except ValueError:
                        end_date = start_date + timedelta(days=30)
                
                campaign = Campaign.objects.create(
                    title=title,
                    description=description,
                    goal_amount=goal_amount,
                    story=story,
                    currency=currency,
                    category=category,
                    creator=request.user,
                    status='draft',
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Handle cover image if uploaded
                if 'cover_image' in request.FILES:
                    campaign.cover_image = request.FILES['cover_image']
                
                campaign.save()
                
                messages.success(request, 'Campaign created successfully!')
                return redirect('main_campaigns:campaign_detail', pk=campaign.pk)
            except Exception as e:
                messages.error(request, f'Error creating campaign: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'create_campaign.html')

@login_required
def edit_campaign(request, pk):
    """Edit an existing campaign."""
    campaign = get_object_or_404(Campaign, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        try:
            # Handle campaign updates
            campaign.title = request.POST.get('title', campaign.title)
            campaign.description = request.POST.get('description', campaign.description)
            campaign.goal_amount = request.POST.get('goal_amount', campaign.goal_amount)
            campaign.story = request.POST.get('story', campaign.story)
            campaign.currency = request.POST.get('currency', campaign.currency)
            campaign.category = request.POST.get('category', campaign.category)
            campaign.status = request.POST.get('status', campaign.status)
            
            # Handle dates if provided
            start_date = request.POST.get('start_date')
            if start_date:
                campaign.start_date = start_date
                
            end_date = request.POST.get('end_date')
            if end_date:
                campaign.end_date = end_date
            
            # Handle cover image if uploaded
            if 'cover_image' in request.FILES:
                campaign.cover_image = request.FILES['cover_image']
            
            campaign.save()
            
            messages.success(request, 'Campaign updated successfully!')
            return redirect('main_campaigns:campaign_detail', pk=campaign.pk)
        except Exception as e:
            messages.error(request, f'Error updating campaign: {str(e)}')
    
    context = {
        'campaign': campaign,
    }
    return render(request, 'edit_campaign.html', context)




