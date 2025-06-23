from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from .models import ReferralBonus
from .serializers import ReferralBonusSerializer
from wallet.models import Wallet

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
        bonuses = ReferralBonus.objects.filter(user=request.user, withdrawn=False)
        total = sum([b.amount for b in bonuses])
        if total < 1000:
            return Response({"message": "Minimum ₦1000 withdrawal required."}, status=400)
        Wallet.objects.get_or_create(user=request.user)[0].credit(total)
        bonuses.update(withdrawn=True)
        return Response({"message": f"₦{total} moved to wallet for withdrawal."})