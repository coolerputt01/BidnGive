from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer
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
