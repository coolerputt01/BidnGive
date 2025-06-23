from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from bids.models import Bid
from referral.models import ReferralBonus
from .models import MergeSettings
from datetime import datetime

class PendingBidsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bids = Bid.objects.filter(status='pending', in_auction_room=True)
        data = [
            {
                "id": b.id,
                "username": b.user.username,
                "amount": b.amount,
                "plan": b.plan,
                "created": b.created_at,
            } for b in bids
        ]
        return Response(data)

class ReferralBonusRequestsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending = ReferralBonus.objects.filter(withdrawn=False).select_related('user')
        response = []
        for bonus in pending:
            user = bonus.user
            response.append({
                'bonus_id': bonus.id,
                'user': user.username,
                'amount': bonus.amount,
                'level': bonus.level,
                'bid_id': bonus.bid_id,
                'account_number': user.account_number,
                'bank': user.bank_name,
            })
        return Response(response)

class ManualMergeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        bid_ids = request.data.get("bid_ids", [])
        bids = Bid.objects.filter(status='pending', in_auction_room=True)
        if not bids:
            return Response({"detail": "No valid pending bids found."}, status=400)
        for bid in bids:
            bid.status = "merged"
            bid.merged_at = datetime.now()
            bid.save()
        return Response({"message": f"{len(bids)} bid(s) merged manually."})