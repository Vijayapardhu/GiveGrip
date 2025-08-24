from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
import json

from .models import Donation, DonationReceipt, DonationGoal, DonationMilestone
from .serializers import (
    DonationReceiptSerializer, DonationSerializer, DonationCreateSerializer,
    DonationUpdateSerializer, DonationGoalSerializer, DonationMilestoneSerializer,
    DonationStatsSerializer, DonationSearchSerializer, DonationAnalyticsSerializer
)
from campaigns.models import Campaign


class DonationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class DonationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing donations
    """
    queryset = Donation.objects.select_related('donor', 'campaign').all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DonationPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return DonationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DonationUpdateSerializer
        return DonationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by campaign if provided
        campaign_id = self.request.query_params.get('campaign_id')
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Filter by donor if provided
        donor_id = self.request.query_params.get('donor_id')
        if donor_id:
            queryset = queryset.filter(donor_id=donor_id)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user)
        
        # Update campaign total amount
        campaign = donation.campaign
        campaign.total_amount = campaign.donations.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        campaign.save()
        
        # Create donation receipt
        DonationReceipt.objects.create(
            donation=donation,
            receipt_number=f"RCPT-{donation.id:06d}",
            amount=donation.amount,
            currency=donation.currency
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a donation"""
        donation = self.get_object()
        
        if donation.donor != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only cancel your own donations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if donation.status != 'pending':
            return Response(
                {'error': 'Only pending donations can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        donation.status = 'cancelled'
        donation.save()
        
        # Update campaign total amount
        campaign = donation.campaign
        campaign.total_amount = campaign.donations.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        campaign.save()
        
        return Response({'message': 'Donation cancelled successfully'})

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Request a refund for a donation"""
        donation = self.get_object()
        
        if donation.donor != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only request refunds for your own donations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if donation.status != 'completed':
            return Response(
                {'error': 'Only completed donations can be refunded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if refund is within time limit (e.g., 30 days)
        days_since_donation = (timezone.now() - donation.created_at).days
        if days_since_donation > 30:
            return Response(
                {'error': 'Refund requests must be made within 30 days'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        donation.status = 'refund_requested'
        donation.save()
        
        return Response({'message': 'Refund request submitted successfully'})


class DonationReceiptViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for donation receipts"""
    queryset = DonationReceipt.objects.select_related('donation', 'donation__donor', 'donation__campaign').all()
    serializer_class = DonationReceiptSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DonationPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by donor if provided
        donor_id = self.request.query_params.get('donor_id')
        if donor_id:
            queryset = queryset.filter(donation__donor_id=donor_id)
        
        # Filter by campaign if provided
        campaign_id = self.request.query_params.get('campaign_id')
        if campaign_id:
            queryset = queryset.filter(donation__campaign_id=campaign_id)
        
        return queryset.order_by('-created_at')


class DonationGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for donation goals"""
    queryset = DonationGoal.objects.select_related('campaign').all()
    serializer_class = DonationGoalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DonationPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by campaign if provided
        campaign_id = self.request.query_params.get('campaign_id')
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        return queryset.order_by('target_amount')


class DonationMilestoneViewSet(viewsets.ModelViewSet):
    """ViewSet for donation milestones"""
    queryset = DonationMilestone.objects.select_related('campaign').all()
    serializer_class = DonationMilestoneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = DonationPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by campaign if provided
        campaign_id = self.request.query_params.get('campaign_id')
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        return queryset.order_by('target_amount')


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def donation_stats(request):
    """Get donation statistics"""
    campaign_id = request.query_params.get('campaign_id')
    
    if campaign_id:
        campaign = get_object_or_404(Campaign, id=campaign_id)
        donations = Donation.objects.filter(campaign=campaign)
    else:
        donations = Donation.objects.all()
    
    # Basic stats
    total_donations = donations.count()
    total_amount = donations.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    avg_donation = donations.filter(status='completed').aggregate(
        avg=Sum('amount') / Count('id')
    )['avg'] or 0
    
    # Status breakdown
    status_breakdown = donations.values('status').annotate(
        count=Count('id'),
        amount=Sum('amount')
    )
    
    # Monthly trends (last 12 months)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    
    monthly_trends = []
    current_date = start_date
    
    while current_date <= end_date:
        month_start = current_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_donations = donations.filter(
            created_at__gte=month_start,
            created_at__lte=month_end,
            status='completed'
        )
        
        monthly_trends.append({
            'month': current_date.strftime('%Y-%m'),
            'count': month_donations.count(),
            'amount': month_donations.aggregate(total=Sum('amount'))['total'] or 0
        })
        
        current_date = (month_start + timedelta(days=32)).replace(day=1)
    
    stats = {
        'total_donations': total_donations,
        'total_amount': total_amount,
        'average_donation': avg_donation,
        'status_breakdown': list(status_breakdown),
        'monthly_trends': monthly_trends
    }
    
    serializer = DonationStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def donation_search(request):
    """Search donations with advanced filters"""
    query = request.query_params.get('q', '')
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')
    payment_method = request.query_params.get('payment_method')
    is_recurring = request.query_params.get('is_recurring')
    
    donations = Donation.objects.select_related('donor', 'campaign').all()
    
    # Text search
    if query:
        donations = donations.filter(
            Q(campaign__title__icontains=query) |
            Q(campaign__description__icontains=query) |
            Q(donor__username__icontains=query) |
            Q(donor__email__icontains=query)
        )
    
    # Amount filters
    if min_amount:
        donations = donations.filter(amount__gte=float(min_amount))
    if max_amount:
        donations = donations.filter(amount__lte=float(max_amount))
    
    # Payment method filter
    if payment_method:
        donations = donations.filter(payment_method=payment_method)
    
    # Recurring filter
    if is_recurring is not None:
        is_recurring_bool = is_recurring.lower() == 'true'
        donations = donations.filter(is_recurring=is_recurring_bool)
    
    # Apply pagination
    paginator = DonationPagination()
    page = paginator.paginate_queryset(donations.order_by('-created_at'), request)
    
    if page is not None:
        serializer = DonationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = DonationSerializer(donations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def donation_analytics(request):
    """Get detailed donation analytics"""
    campaign_id = request.query_params.get('campaign_id')
    period = request.query_params.get('period', '30d')  # 7d, 30d, 90d, 1y
    
    # Calculate date range based on period
    end_date = timezone.now()
    if period == '7d':
        start_date = end_date - timedelta(days=7)
    elif period == '30d':
        start_date = end_date - timedelta(days=30)
    elif period == '90d':
        start_date = end_date - timedelta(days=90)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    
    if campaign_id:
        campaign = get_object_or_404(Campaign, id=campaign_id)
        donations = Donation.objects.filter(
            campaign=campaign,
            created_at__gte=start_date,
            created_at__lte=end_date
        )
    else:
        donations = Donation.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )
    
    # Daily trends
    daily_trends = []
    current_date = start_date
    
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        day_donations = donations.filter(
            created_at__gte=current_date,
            created_at__lt=next_date,
            status='completed'
        )
        
        daily_trends.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'count': day_donations.count(),
            'amount': day_donations.aggregate(total=Sum('amount'))['total'] or 0
        })
        
        current_date = next_date
    
    # Top donors
    top_donors = donations.filter(status='completed').values(
        'donor__username', 'donor__email'
    ).annotate(
        total_donated=Sum('amount'),
        donation_count=Count('id')
    ).order_by('-total_donated')[:10]
    
    # Payment method distribution
    payment_methods = donations.filter(status='completed').values(
        'payment_method'
    ).annotate(
        count=Count('id'),
        amount=Sum('amount')
    ).order_by('-amount')
    
    # Campaign performance (if no specific campaign)
    if not campaign_id:
        campaign_performance = donations.filter(status='completed').values(
            'campaign__title', 'campaign__id'
        ).annotate(
            total_amount=Sum('amount'),
            donor_count=Count('donor', distinct=True)
        ).order_by('-total_amount')[:10]
    else:
        campaign_performance = []
    
    analytics = {
        'period': period,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'daily_trends': daily_trends,
        'top_donors': list(top_donors),
        'payment_methods': list(payment_methods),
        'campaign_performance': campaign_performance,
        'summary': {
            'total_donations': donations.count(),
            'completed_donations': donations.filter(status='completed').count(),
            'total_amount': donations.filter(status='completed').aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'unique_donors': donations.values('donor').distinct().count()
        }
    }
    
    serializer = DonationAnalyticsSerializer(analytics)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_donations(request):
    """Get donations for the authenticated user"""
    donations = Donation.objects.filter(donor=request.user).select_related(
        'campaign'
    ).order_by('-created_at')
    
    paginator = DonationPagination()
    page = paginator.paginate_queryset(donations, request)
    
    if page is not None:
        serializer = DonationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = DonationSerializer(donations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_donation_history(request):
    """Get detailed donation history for the authenticated user"""
    donations = Donation.objects.filter(donor=request.user).select_related(
        'campaign'
    ).order_by('-created_at')
    
    # Group by year and month
    history = {}
    for donation in donations:
        year = donation.created_at.year
        month = donation.created_at.month
        
        if year not in history:
            history[year] = {}
        if month not in history[year]:
            history[year][month] = {
                'donations': [],
                'total_amount': 0,
                'count': 0
            }
        
        history[year][month]['donations'].append({
            'id': donation.id,
            'campaign_title': donation.campaign.title,
            'amount': donation.amount,
            'status': donation.status,
            'created_at': donation.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        if donation.status == 'completed':
            history[year][month]['total_amount'] += donation.amount
            history[year][month]['count'] += 1
    
    # Convert to sorted list
    sorted_history = []
    for year in sorted(history.keys(), reverse=True):
        year_data = {'year': year, 'months': []}
        for month in sorted(history[year].keys(), reverse=True):
            month_data = {
                'month': month,
                'month_name': datetime(year, month, 1).strftime('%B'),
                **history[year][month]
            }
            year_data['months'].append(month_data)
        sorted_history.append(year_data)
    
    return Response({
        'donation_history': sorted_history,
        'total_donations': donations.count(),
        'total_amount': donations.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_donation_preferences(request, donation_id):
    """Update donation preferences (anonymous, message, etc.)"""
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    
    if donation.status != 'pending':
        return Response(
            {'error': 'Only pending donations can be updated'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = DonationUpdateSerializer(donation, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_donations(request):
    """Get recent donations for the authenticated user."""
    user = request.user
    
    # Get recent completed donations
    recent_donations = Donation.objects.filter(
        donor=user,
        status='completed'
    ).select_related('campaign').order_by('-created_at')[:10]
    
    donations_data = []
    for donation in recent_donations:
        donations_data.append({
            'id': donation.id,
            'campaign_title': donation.campaign.title,
            'amount': float(donation.amount),
            'status': donation.status,
            'created_at': donation.created_at.isoformat(),
            'campaign_id': donation.campaign.id
        })
    
    return Response(donations_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_donation_stats(request, campaign_id):
    """Get donation statistics for a specific campaign."""
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    # Get campaign donations
    donations = Donation.objects.filter(campaign=campaign, status='completed')
    
    # Calculate statistics
    total_donations = donations.count()
    total_amount = donations.aggregate(total=Sum('amount'))['total'] or 0
    avg_donation = total_amount / total_donations if total_donations > 0 else 0
    
    # Monthly breakdown
    monthly_stats = donations.extra(
        select={'year': "EXTRACT(year FROM created_at)", 'month': "EXTRACT(month FROM created_at)"}
    ).values('year', 'month').annotate(
        count=Count('id'),
        amount=Sum('amount')
    ).order_by('year', 'month')
    
    # Top donors
    top_donors = donations.values('donor__first_name', 'donor__last_name').annotate(
        total_amount=Sum('amount'),
        donation_count=Count('id')
    ).order_by('-total_amount')[:10]
    
    return Response({
        'campaign_id': campaign_id,
        'campaign_title': campaign.title,
        'total_donations': total_donations,
        'total_amount': float(total_amount),
        'average_donation': float(avg_donation),
        'monthly_breakdown': list(monthly_stats),
        'top_donors': list(top_donors)
    })




