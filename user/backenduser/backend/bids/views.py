from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from django.core.management import call_command

from .models import Bid
from .serializers import BidSerializer, PaymentProofSerializer, ConfirmPaymentSerializer
from wallet.models import Wallet, WalletTransaction
from referral.utils import award_referral_bonus  # Referral logic

# ================================
# Main ViewSet for User Bids
# ================================
class BidViewSet(viewsets.ModelViewSet):
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        has_unpaid_bid = Bid.objects.filter(user=user).exclude(status='paid').exists()
        if has_unpaid_bid:
            raise ValidationError("You already have a pending or unpaid bid.")

        amount = serializer.validated_data['amount']
        plan = serializer.validated_data['plan']
        expected_return = Decimal(amount) * Decimal('1.5') if plan == '50_24' else Decimal('0')

        serializer.save(user=user, expected_return=expected_return)

# ================================
# Upload Proof of Payment (Image)
# ================================
class UploadProofView(generics.UpdateAPIView):
    serializer_class = PaymentProofSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]  # Enables image uploads via multipart/form-data

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user, status='merged')

# ================================
# Receiver Confirms a Payment
# ================================
class ConfirmReceiverView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bid_id):
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response({"error": "Bid not found."}, status=404)

        if bid.user == request.user:
            return Response({"error": "You can't confirm your own bid as receiver."}, status=403)

        serializer = ConfirmPaymentSerializer(instance=bid, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ✅ Award referral bonus only once on first paid investment
        if bid.type == 'investment':
            bid.status = 'paid'
            bid.paid_at = timezone.now()
            bid.save()
            award_referral_bonus(bid)

        # ✅ If withdrawal, credit the user's wallet
        if bid.type == 'withdrawal':
            bid.status = 'paid'
            bid.paid_at = timezone.now()
            wallet, _ = Wallet.objects.get_or_create(user=bid.user)
            wallet.balance += bid.amount
            wallet.save()

            WalletTransaction.objects.create(
                user=bid.user,
                wallet=wallet,
                amount=bid.amount,
                type='credit',
                description='Wallet withdrawal via P2P'
            )

        return Response({"message": "Payment confirmed by receiver."})

# ================================
# Withdraw Referral Bonus (P2P)
# ================================
class WithdrawBidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')

        if not amount:
            return Response({'error': 'Amount is required'}, status=400)

        try:
            amount = Decimal(amount)
        except:
            return Response({'error': 'Invalid amount format'}, status=400)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        if wallet.balance < amount:
            return Response({'error': 'Insufficient balance'}, status=400)

        wallet.balance -= amount
        wallet.save()

        Bid.objects.create(
            user=request.user,
            amount=amount,
            plan='withdrawal',
            type='withdrawal',
            expected_return=0,
            status='pending'
        )

        return Response({'message': f'₦{amount} withdrawal bid created successfully.'})

# ================================
# Admin Endpoint: Auto Merge
# ================================
@api_view(['GET'])
@permission_classes([AllowAny])
def run_auto_merge(request):
    if request.GET.get('key') != 'biddedkey':
        return Response({'error': 'Unauthorized'}, status=403)
    call_command('auto_merge')
    return Response({'status': 'Auto merge completed.'})

# ================================
# Admin Endpoint: Auto Block Expired
# ================================
@api_view(['GET'])
@permission_classes([AllowAny])
def auto_block(request):
    if request.GET.get('key') != 'expiredkey':
        return Response({'error': 'Unauthorized'}, status=403)
    call_command('auto_block_expired')
    return Response({'status': 'Expired bids auto-block executed.'})

@api_view(['GET'])
@permission_classes([AllowAny])  # Optional: protect with admin if needed
def complete_paid_bids(request):
    if request.GET.get('key') != 'completekey':
        return Response({'error': 'Unauthorized'}, status=403)

    call_command('complete_paid_bids')
    return Response({'status': 'Completed paid bids marked successfully'})
