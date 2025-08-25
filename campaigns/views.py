from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from .models import Campaign, CampaignCategory, CampaignImage, CampaignUpdate
from .serializers import (
    CampaignSerializer, CampaignCreateSerializer, CampaignUpdateSerializer,
    CampaignDetailSerializer, CampaignCategorySerializer, CampaignImageSerializer,
    CampaignUpdateSerializer as CampaignUpdateModelSerializer,
    CampaignImageCreateSerializer, CampaignUpdateCreateSerializer,
    CampaignSearchSerializer
)


class CampaignCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for CampaignCategory model."""
    
    queryset = CampaignCategory.objects.filter(is_active=True)
    serializer_class = CampaignCategorySerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['get'])
    def campaigns(self, request, pk=None):
        """Get campaigns in a specific category."""
        category = self.get_object()
        campaigns = Campaign.objects.filter(category=category, status='active')
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


class CampaignViewSet(viewsets.ModelViewSet):
    """ViewSet for Campaign model."""
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'is_featured', 'is_verified', 'currency']
    search_fields = ['title', 'description', 'story']
    ordering_fields = ['created_at', 'goal_amount', 'current_amount', 'end_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CampaignUpdateSerializer
        elif self.action == 'retrieve':
            return CampaignDetailSerializer
        return CampaignSerializer
    
    def get_queryset(self):
        """Filter campaigns based on user permissions."""
        queryset = super().get_queryset()
        
        # If user is not authenticated, only show active campaigns
        if not self.request.user.is_authenticated:
            return queryset.filter(status='active')
        
        # If user is staff, show all campaigns
        if self.request.user.is_staff:
            return queryset
        
        # For regular users, show active campaigns and their own campaigns
        return queryset.filter(
            Q(status='active') | Q(creator=self.request.user)
        )
    
    def perform_create(self, serializer):
        """Set the creator when creating a campaign."""
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment campaign view count."""
        campaign = self.get_object()
        campaign.view_count = F('view_count') + 1
        campaign.save()
        campaign.refresh_from_db()
        return Response({'view_count': campaign.view_count})
    
    @action(detail=True, methods=['post'])
    def increment_share(self, request, pk=None):
        """Increment campaign share count."""
        campaign = self.get_object()
        campaign.share_count = F('share_count') + 1
        campaign.save()
        campaign.refresh_from_db()
        return Response({'share_count': campaign.share_count})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured campaigns."""
        campaigns = self.get_queryset().filter(is_featured=True, status='active')
        serializer = self.get_serializer(campaigns, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending campaigns (based on views and donations)."""
        campaigns = self.get_queryset().filter(status='active').order_by(
            '-view_count', '-donor_count', '-current_amount'
        )[:10]
        serializer = self.get_serializer(campaigns, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ending_soon(self, request):
        """Get campaigns ending soon."""
        from django.utils import timezone
        from datetime import timedelta
        
        # Get campaigns ending in the next 7 days
        end_date = timezone.now() + timedelta(days=7)
        campaigns = self.get_queryset().filter(
            status='active',
            end_date__lte=end_date
        ).order_by('end_date')
        
        serializer = self.get_serializer(campaigns, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Advanced campaign search."""
        serializer = CampaignSearchSerializer(data=request.data)
        if serializer.is_valid():
            queryset = self.get_queryset()
            
            # Apply search filters
            if serializer.validated_data.get('query'):
                query = serializer.validated_data['query']
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(story__icontains=query)
                )
            
            if serializer.validated_data.get('category'):
                queryset = queryset.filter(category__name__icontains=serializer.validated_data['category'])
            
            if serializer.validated_data.get('min_amount'):
                queryset = queryset.filter(goal_amount__gte=serializer.validated_data['min_amount'])
            
            if serializer.validated_data.get('max_amount'):
                queryset = queryset.filter(goal_amount__lte=serializer.validated_data['max_amount'])
            
            if serializer.validated_data.get('status'):
                queryset = queryset.filter(status=serializer.validated_data['status'])
            
            if serializer.validated_data.get('featured') is not None:
                queryset = queryset.filter(is_featured=serializer.validated_data['featured'])
            
            if serializer.validated_data.get('verified') is not None:
                queryset = queryset.filter(is_verified=serializer.validated_data['verified'])
            
            # Paginate results
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampaignImageViewSet(viewsets.ModelViewSet):
    """ViewSet for CampaignImage model."""
    
    serializer_class = CampaignImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_pk')
        return CampaignImage.objects.filter(campaign_id=campaign_id)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignImageCreateSerializer
        return CampaignImageSerializer
    
    def perform_create(self, serializer):
        campaign_id = self.kwargs.get('campaign_pk')
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        serializer.save(campaign=campaign)


class CampaignUpdateViewSet(viewsets.ModelViewSet):
    """ViewSet for CampaignUpdate model."""
    
    serializer_class = CampaignUpdateModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_pk')
        return CampaignUpdate.objects.filter(campaign_id=campaign_id)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignUpdateCreateSerializer
        return CampaignUpdateModelSerializer
    
    def perform_create(self, serializer):
        campaign_id = self.kwargs.get('campaign_pk')
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        serializer.save(campaign=campaign)





        # Filter by status
        status_filter = self.request.query_params.get('status', 'active')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by amount range
        min_amount = self.request.query_params.get('min_amount')
        if min_amount:
            queryset = queryset.filter(goal_amount__gte=min_amount)
        
        max_amount = self.request.query_params.get('max_amount')
        if max_amount:
            queryset = queryset.filter(goal_amount__lte=max_amount)
        
        # Filter featured campaigns
        featured_only = self.request.query_params.get('featured_only', '').lower() == 'true'
        if featured_only:
            queryset = queryset.filter(is_featured=True)
        
        # Filter verified campaigns
        verified_only = self.request.query_params.get('verified_only', '').lower() == 'true'
        if verified_only:
            queryset = queryset.filter(is_verified=True)
        
        return queryset


class CampaignDetailView(generics.RetrieveAPIView):
    """Retrieve a specific campaign."""
    
    queryset = Campaign.objects.select_related('category').prefetch_related(
        'updates', 'comments', 'shares'
    )
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CampaignCreateView(generics.CreateAPIView):
    """Create a new campaign."""
    
    serializer_class = CampaignCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set campaign creator and status."""
        serializer.save(
            creator_email=self.request.user.email,
            status='draft'
        )


class CampaignUpdateView(generics.UpdateAPIView):
    """Update an existing campaign."""
    
    queryset = Campaign.objects.all()
    serializer_class = CampaignCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Only allow campaign creators to update."""
        return Campaign.objects.filter(creator_email=self.request.user.email)


class CampaignUpdateListView(generics.ListCreateAPIView):
    """List and create campaign updates."""
    
    serializer_class = CampaignUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        campaign_slug = self.kwargs.get('campaign_slug')
        campaign = get_object_or_404(Campaign, slug=campaign_slug)
        return CampaignUpdate.objects.filter(campaign=campaign, is_public=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignUpdateCreateSerializer
        return CampaignUpdateSerializer
    
    def perform_create(self, serializer):
        campaign_slug = self.kwargs.get('campaign_slug')
        campaign = get_object_or_404(Campaign, slug=campaign_slug)
        serializer.save(campaign=campaign)


class CampaignCommentListView(generics.ListCreateAPIView):
    """List and create campaign comments."""
    
    serializer_class = CampaignCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        campaign_slug = self.kwargs.get('campaign_slug')
        campaign = get_object_or_404(Campaign, slug=campaign_slug)
        return CampaignComment.objects.filter(campaign=campaign, is_approved=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CampaignCommentCreateSerializer
        return CampaignCommentSerializer
    
    def perform_create(self, serializer):
        campaign_slug = self.kwargs.get('campaign_slug')
        campaign = get_object_or_404(Campaign, slug=campaign_slug)
        serializer.save(campaign=campaign, user=self.request.user)


class CampaignShareView(APIView):
    """Share a campaign on social media."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, campaign_slug):
        campaign = get_object_or_404(Campaign, slug=campaign_slug)
        
        serializer = CampaignShareCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Create share record
            CampaignShare.objects.create(
                campaign=campaign,
                platform=serializer.validated_data['platform'],
                user=request.user if request.user.is_authenticated else None,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return Response({
                'message': f'Campaign shared on {serializer.validated_data["platform"]}'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeaturedCampaignsView(generics.ListAPIView):
    """Get featured campaigns."""
    
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Campaign.objects.filter(
            is_featured=True,
            status='active'
        ).select_related('category').prefetch_related('updates')


class CampaignSearchView(APIView):
    """Advanced campaign search."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CampaignSearchSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            queryset = Campaign.objects.select_related('category').prefetch_related(
                'updates', 'comments', 'shares'
            )
            
            # Apply filters
            if data.get('query'):
                query = data['query']
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(story__icontains=query) |
                    Q(creator_name__icontains=query) |
                    Q(creator_organization__icontains=query)
                )
            
            if data.get('category'):
                queryset = queryset.filter(category_id=data['category'])
            
            if data.get('min_amount'):
                queryset = queryset.filter(goal_amount__gte=data['min_amount'])
            
            if data.get('max_amount'):
                queryset = queryset.filter(goal_amount__lte=data['max_amount'])
            
            if data.get('status'):
                queryset = queryset.filter(status=data['status'])
            
            if data.get('featured_only'):
                queryset = queryset.filter(is_featured=True)
            
            if data.get('verified_only'):
                queryset = queryset.filter(is_verified=True)
            
            # Apply sorting
            sort_by = data.get('sort_by', 'newest')
            if sort_by == 'newest':
                queryset = queryset.order_by('-created_at')
            elif sort_by == 'oldest':
                queryset = queryset.order_by('created_at')
            elif sort_by == 'goal_amount':
                queryset = queryset.order_by('-goal_amount')
            elif sort_by == 'current_amount':
                queryset = queryset.order_by('-current_amount')
            elif sort_by == 'days_remaining':
                queryset = queryset.order_by('end_date')
            elif sort_by == 'popularity':
                queryset = queryset.annotate(
                    total_donors=Count('donations', filter=Q(donations__status='completed'))
                ).order_by('-total_donors')
            
            # Pagination
            page = data.get('page', 1)
            page_size = data.get('page_size', 20)
            start = (page - 1) * page_size
            end = start + page_size
            
            total_count = queryset.count()
            campaigns = queryset[start:end]
            
            serializer = CampaignSerializer(campaigns, many=True)
            
            return Response({
                'campaigns': serializer.data,
                'total_count': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_count + page_size - 1) // page_size
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def campaign_stats(request, campaign_slug):
    """Get campaign statistics."""
    campaign = get_object_or_404(Campaign, slug=campaign_slug)
    
    # Calculate statistics
    total_donations = campaign.donations.filter(status='completed').count()
    total_amount = campaign.donations.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Recent donations
    recent_donations = campaign.donations.filter(
        status='completed'
    ).select_related('donor').order_by('-created_at')[:5]
    
    recent_data = []
    for donation in recent_donations:
        recent_data.append({
            'amount': donation.amount,
            'donor_name': donation.donor.full_name if donation.donor.first_name else 'Anonymous',
            'date': donation.created_at
        })
    
    stats = {
        'total_donations': total_donations,
        'total_amount': total_amount,
        'goal_amount': campaign.goal_amount,
        'progress_percentage': campaign.progress_percentage,
        'days_remaining': campaign.days_remaining,
        'total_donors': campaign.total_donors,
        'recent_donations': recent_data
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_campaign_progress(request):
    """Get campaigns that the authenticated user has donated to."""
    user = request.user
    
    # Get campaigns where user has made donations
    user_campaigns = Campaign.objects.filter(
        donations__donor=user,
        donations__status='completed'
    ).distinct().annotate(
        user_donated=Sum('donations__amount', filter=Q(donations__donor=user, donations__status='completed'))
    ).order_by('-donations__created_at')[:10]
    
    campaigns_data = []
    for campaign in user_campaigns:
        campaigns_data.append({
            'id': campaign.id,
            'title': campaign.title,
            'goal': float(campaign.goal_amount),
            'raised': float(campaign.current_amount),
            'progress_percentage': campaign.progress_percentage,
            'days_remaining': campaign.days_remaining,
            'user_donated': float(campaign.user_donated or 0)
        })
    
    return Response(campaigns_data)




