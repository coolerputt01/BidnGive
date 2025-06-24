from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from bids.models import Bid
from referral.models import ReferralBonus ,WithdrawalRequest
from .models import MergeSettings
from datetime import datetime, time, timedelta

class AuctionStatusView(APIView):
    def get(self, request):
        settings = MergeSettings.objects.last()
        
        # Use default times if not set
        morning = settings.morning_time if settings else time(8, 0)
        evening = settings.evening_time if settings else time(18, 30)
        
        now = datetime.now()
        now_time = now.time()

        def next_auction(now_time, morning, evening):
            today = datetime.today()
            morning_dt = datetime.combine(today, morning)
            evening_dt = datetime.combine(today, evening)

            if now_time < morning:
                return morning_dt
            elif now_time < evening:
                return evening_dt
            else:
                return morning_dt + timedelta(days=1)

        next_time = next_auction(now_time, morning, evening)
        time_diff = next_time - now
        remaining_seconds = max(0, int(time_diff.total_seconds()))

        # Calculate auction window (30 minutes)
        def in_window(start_time):
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()
            return start_time <= now_time <= end_time

        is_open = in_window(morning) or in_window(evening)

        return Response({
            "market_status": "open" if is_open else "closed",
            "next_auction": next_time.strftime("%I:%M %p"),
            "remaining_seconds": remaining_seconds
        })

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
    
class MarkWithdrawalPaidView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, withdrawal_id):
        try:
            wd = WithdrawalRequest.objects.get(id=withdrawal_id, status='pending')
            wd.status = 'paid'
            wd.save()
            return Response({'message': f'Withdrawal #{withdrawal_id} marked as paid.'})
        except WithdrawalRequest.DoesNotExist:
            return Response({'error': 'Withdrawal not found or already processed.'}, status=404)

class PendingWithdrawalsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending = WithdrawalRequest.objects.filter(status='pending').select_related('user')
        data = [
            {
                'id': w.id,
                'user': w.user.username,
                'email': w.user.email,
                'amount': float(w.amount),
                'requested_at': w.requested_at,
            } for w in pending
        ]
        return Response(data)

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