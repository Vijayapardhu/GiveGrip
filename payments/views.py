"""
Views for the payments application.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings
import json
import logging

from .models import (
    PaymentMethod, PaymentTransaction, PaymentRefund, 
    PaymentWebhook, PaymentGatewayConfig
)
from .serializers import (
    PaymentMethodSerializer, PaymentMethodCreateSerializer, PaymentMethodUpdateSerializer,
    PaymentTransactionSerializer, PaymentTransactionCreateSerializer,
    PaymentRefundSerializer, PaymentRefundCreateSerializer,
    PaymentWebhookSerializer, PaymentGatewayConfigSerializer,
    PaymentMethodListSerializer, PaymentSummarySerializer
)
from donations.models import Donation
from users.models import User

logger = logging.getLogger(__name__)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payment methods.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return payment methods for the authenticated user."""
        return PaymentMethod.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PaymentMethodCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PaymentMethodUpdateSerializer
        return PaymentMethodSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a payment method."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set a payment method as default."""
        payment_method = self.get_object()
        
        # Remove default from other payment methods
        PaymentMethod.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # Set this one as default
        payment_method.is_default = True
        payment_method.save()
        
        return Response({'message': 'Payment method set as default'})
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a payment method (e.g., with a small test charge)."""
        payment_method = self.get_object()
        
        try:
            # Here you would implement payment method verification
            # For now, we'll just mark it as verified
            payment_method.is_verified = True
            payment_method.save()
            
            return Response({'message': 'Payment method verified successfully'})
        except Exception as e:
            logger.error(f"Error verifying payment method: {e}")
            return Response(
                {'error': 'Failed to verify payment method'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payment transactions.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return transactions for the authenticated user."""
        return PaymentTransaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PaymentTransactionCreateSerializer
        return PaymentTransactionSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a transaction."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def capture(self, request, pk=None):
        """Capture a pending transaction."""
        transaction = self.get_object()
        
        if transaction.status != PaymentStatus.PENDING:
            return Response(
                {'error': 'Only pending transactions can be captured'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Here you would implement the actual capture logic
            transaction.status = PaymentStatus.COMPLETED
            transaction.captured_at = timezone.now()
            transaction.save()
            
            return Response({'message': 'Transaction captured successfully'})
        except Exception as e:
            logger.error(f"Error capturing transaction: {e}")
            return Response(
                {'error': 'Failed to capture transaction'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        """Void a pending transaction."""
        transaction = self.get_object()
        
        if transaction.status != PaymentStatus.PENDING:
            return Response(
                {'error': 'Only pending transactions can be voided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Here you would implement the actual void logic
            transaction.status = PaymentStatus.VOIDED
            transaction.voided_at = timezone.now()
            transaction.save()
            
            return Response({'message': 'Transaction voided successfully'})
        except Exception as e:
            logger.error(f"Error voiding transaction: {e}")
            return Response(
                {'error': 'Failed to void transaction'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentRefundViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payment refunds.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return refunds for the authenticated user."""
        return PaymentRefund.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PaymentRefundCreateSerializer
        return PaymentRefundSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a refund."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a refund."""
        refund = self.get_object()
        
        if refund.status != PaymentStatus.PENDING:
            return Response(
                {'error': 'Only pending refunds can be processed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Here you would implement the actual refund processing
            refund.status = PaymentStatus.COMPLETED
            refund.processed_at = timezone.now()
            refund.save()
            
            return Response({'message': 'Refund processed successfully'})
        except Exception as e:
            logger.error(f"Error processing refund: {e}")
            return Response(
                {'error': 'Failed to process refund'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


def process_payment(request):
    """
    Process a payment for a donation.
    """
    if request.method != 'POST':
        return Response(
            {'error': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    try:
        data = json.loads(request.body)
        donation_id = data.get('donation_id')
        payment_method_id = data.get('payment_method_id')
        amount = data.get('amount')
        
        # Validate required fields
        if not all([donation_id, payment_method_id, amount]):
            return Response(
                {'error': 'Missing required fields'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the donation and payment method
        donation = get_object_or_404(Donation, id=donation_id)
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        
        # Verify the user owns both the donation and payment method
        if donation.user != request.user or payment_method.user != request.user:
            return Response(
                {'error': 'Access denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify amount matches donation amount
        if float(amount) != float(donation.amount):
            return Response(
                {'error': 'Amount mismatch'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Create the transaction
            transaction = PaymentTransaction.objects.create(
                user=request.user,
                donation=donation,
                payment_method=payment_method,
                amount=amount,
                currency=donation.currency,
                gateway=payment_method.gateway,
                status=PaymentStatus.PENDING
            )
            
            # Here you would integrate with the actual payment gateway
            # For now, we'll simulate a successful payment
            transaction.status = PaymentStatus.COMPLETED
            transaction.completed_at = timezone.now()
            transaction.save()
            
            # Update donation status
            donation.status = 'completed'
            donation.save()
            
            return Response({
                'success': True,
                'transaction_id': transaction.id,
                'message': 'Payment processed successfully'
            })
            
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        return Response(
            {'error': 'Payment processing failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def payment_webhook(request, gateway):
    """
    Handle payment gateway webhooks.
    """
    if request.method != 'POST':
        return Response(
            {'error': 'Method not allowed'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    try:
        # Verify webhook signature (implement based on gateway)
        # This is a simplified example
        
        data = json.loads(request.body)
        webhook_type = data.get('type')
        transaction_id = data.get('transaction_id')
        
        # Create webhook record
        PaymentWebhook.objects.create(
            gateway=gateway,
            payload=data,
            webhook_type=webhook_type,
            transaction_id=transaction_id
        )
        
        # Process webhook based on type
        if webhook_type == 'payment.succeeded':
            # Handle successful payment
            pass
        elif webhook_type == 'payment.failed':
            # Handle failed payment
            pass
        elif webhook_type == 'refund.processed':
            # Handle refund
            pass
        
        return Response({'success': True})
        
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response(
            {'error': 'Webhook processing failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def payment_summary(request):
    """
    Get payment summary for the authenticated user.
    """
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        # Get payment summary data
        total_transactions = PaymentTransaction.objects.filter(user=request.user).count()
        total_amount = PaymentTransaction.objects.filter(
            user=request.user, 
            status=PaymentStatus.COMPLETED
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get recent transactions
        recent_transactions = PaymentTransaction.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        
        summary_data = {
            'total_transactions': total_transactions,
            'total_amount': float(total_amount),
            'recent_transactions': PaymentTransactionSerializer(recent_transactions, many=True).data
        }
        
        serializer = PaymentSummarySerializer(summary_data)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error getting payment summary: {e}")
        return Response(
            {'error': 'Failed to get payment summary'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def payment_methods_list(request):
    """
    Get list of available payment methods for the authenticated user.
    """
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        serializer = PaymentMethodListSerializer(payment_methods, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error getting payment methods: {e}")
        return Response(
            {'error': 'Failed to get payment methods'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




