from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from .models import ReferralBonus , WithdrawalRequest
from .serializers import ReferralBonusSerializer
from wallet.models import Wallet
from decimal import Decimal

class LoginBonusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = now().date()
        if user.last_login_bonus == today:
            return Response({'message': 'Bonus already claimed today.'})
        user.last_login_bonus = today
        user.save()

        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.balance += 100
        wallet.save()

        return Response({'message': '₦100 login bonus credited.'})

class ReferralBonusListView(generics.ListAPIView):
    serializer_class = ReferralBonusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReferralBonus.objects.filter(user=self.request.user)

class RequestReferralWithdrawal(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        bank = request.data.get("bank")
        account = request.data.get("account")
        amount = request.data.get("amount")

        try:
            amount = Decimal(amount)
        except:
            return Response({"message": "Invalid amount format."}, status=400)

        if amount < 1000:
            return Response({"message": "Minimum withdrawal is ₦1000"}, status=400)

        wallet = Wallet.objects.get_or_create(user=user)[0]

        if wallet.balance < amount:
            return Response({"message": "Insufficient wallet balance"}, status=400)

        # Deduct balance and create request
        wallet.balance -= amount
        wallet.save()

        WithdrawalRequest.objects.create(
            user=user,
            bank=bank,
            account=account,
            amount=amount,
        )

        return Response({"message": "Withdrawal request submitted successfully."}, status=status.HTTP_200_OK)