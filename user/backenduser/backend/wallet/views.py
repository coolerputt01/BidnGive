from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet ,WalletTransaction
from .serializers import WalletSerializer , WalletTransactionSerializer
from referral.models import ReferralBonus
from bids.models import Bid
from django.utils import timezone

class WalletBalanceView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet

class DailyBonusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        today = timezone.now().date()
        if wallet.last_bonus_date == today:
            return Response({"message": "Already claimed today"}, status=400)
        wallet.credit(100)
        wallet.last_bonus_date = today
        wallet.save()
        return Response({"message": "Bonus credited", "balance": wallet.balance})

class WithdrawalHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletTransactionSerializer

    def get_queryset(self):
        return WalletTransaction.objects.filter(user=self.request.user, type='debit')

class InvestFromReferralView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        plan = request.data.get('plan')

        if not amount or not plan:
            return Response({'error': 'Amount and plan are required.'}, status=400)

        bonuses = ReferralBonus.objects.filter(user=request.user, withdrawn=False)
        total_bonus = sum(b.amount for b in bonuses)

        if total_bonus < 10000:
            return Response({'error': 'Referral bonus must be at least ₦10,000 to invest.'}, status=400)

        if total_bonus < float(amount):
            return Response({'error': 'Insufficient referral bonus balance.'}, status=400)

        # Mark bonuses as withdrawn (or handle in your custom way)
        for b in bonuses:
            b.withdrawn = True
            b.save()

        # Optionally, credit to wallet first (or skip this if directly investing)
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += float(amount)
        wallet.save()

        WalletTransaction.objects.create(
            user=request.user,
            wallet=wallet,
            amount=amount,
            type='credit',
            description='Referral bonus invested'
        )

        Bid.objects.create(
            user=request.user,
            amount=amount,
            plan=plan,
            status='pending'
        )

        return Response({'message': f'Successfully invested ₦{amount} from referral bonus.'})
