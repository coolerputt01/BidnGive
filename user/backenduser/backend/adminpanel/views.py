from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from bids.models import Bid
from referral.models import ReferralBonus ,WithdrawalRequest
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MergeSettings
from datetime import datetime, time, timedelta
from accounts.models import User
from accounts.serializers import UserSerializer

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
    
class AllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)

class PendingBidsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bids = Bid.objects.filter(status='pending', user__in_auction_room=True)
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

class ManualMergeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        bid_ids = request.data.get("bid_ids", [])
        if not bid_ids:
            return Response({"detail": "No bid IDs provided."}, status=400)

        bids = Bid.objects.filter(
            id__in=bid_ids,
            status='pending',
            user__in_auction_room=True
        )

        if not bids.exists():
            return Response({"detail": "No valid pending bids found."}, status=400)

        merged_count = 0
        for bid in bids:
            bid.status = "merged"
            bid.merged_at = datetime.now()
            bid.save()
            merged_count += 1

        return Response({"message": f"{merged_count} bid(s) merged manually."})

class UpdateMergeSettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = MergeSettings.objects.last()
        return Response({
            "morning_time": settings.morning_time.strftime('%H:%M'),
            "evening_time": settings.evening_time.strftime('%H:%M'),
        })

    def patch(self, request):
        settings = MergeSettings.objects.last()
        morning = request.data.get("morning_time")
        evening = request.data.get("evening_time")

        if morning:
            settings.morning_time = morning
        if evening:
            settings.evening_time = evening

        settings.save()

class CreateInvestmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount')
        plan = request.data.get('plan')

        if not (email and amount and plan):
            return Response({'error': 'Email, amount, and plan are required.'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        Bid.objects.create(user=user, amount=amount, plan=plan, status='merged')  # Directly mark as merged

        return Response({'message': f'Investment of ₦{amount} created for {email} under "{plan}" plan.'})
    
class CancelInvestmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        bid_id = request.data.get("bid_id")
        if not bid_id:
            return Response({'error': 'Bid ID is required.'}, status=400)

        try:
            bid = Bid.objects.get(id=bid_id)
            if bid.status in ['cancelled', 'paid']:
                return Response({'error': 'Cannot cancel this bid.'}, status=400)
            bid.status = 'cancelled'
            bid.save()
            return Response({'message': f'Bid #{bid_id} cancelled.'})
        except Bid.DoesNotExist:
            return Response({'error': 'Bid not found.'}, status=404)

class BlockUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            user.is_disabled = True
            user.save()
            return Response({"message": f"{user.username} has been blocked."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UnblockUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            user.is_disabled = False
            user.save()
            return Response({"message": f"{user.username} has been unblocked."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class LoginAsUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_disabled:
                return Response({"error": "This user is blocked."}, status=403)
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)