# adminpanel/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, time, timedelta
from django.utils import timezone

from accounts.models import User
from accounts.serializers import UserSerializer
from bids.models import Bid
from bids.serializers import BidSerializer
from referral.models import ReferralBonus, WithdrawalRequest
from .models import MergeSettings
from django.utils import timezone
from .merge import merge_new_investment
from django.contrib.auth.hashers import make_password

class AuctionStatusView(APIView):
    def get(self, request):
        settings = MergeSettings.objects.last()
        now = timezone.localtime()
        now_time = now.time()

        morning = settings.morning_time if settings else time(8, 0)
        evening = settings.evening_time if settings else time(20, 00)

        def get_next_auction():
            today = now.date()
            morning_dt = timezone.make_aware(datetime.combine(today, morning))
            evening_dt = timezone.make_aware(datetime.combine(today, evening))

            if now_time < morning:
                return morning_dt
            elif now_time < evening:
                return evening_dt
            return timezone.make_aware(datetime.combine(today + timedelta(days=1), morning))

        def is_open_window(auction_time):
            end = (datetime.combine(now.date(), auction_time) + timedelta(minutes=30)).time()
            return auction_time <= now_time <= end

        next_time = get_next_auction()
        remaining_seconds = max(0, int((next_time - now).total_seconds()))
        is_open = is_open_window(morning) or is_open_window(evening)

        return Response({
            "market_status": "open" if is_open else "closed",
            "next_auction": next_time.strftime("%I:%M %p"),
            "remaining_seconds": remaining_seconds
        })

class ChangeUserPasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        if not all([email, new_password]):
            return Response({"error": "Email and new password are required."}, status=400)

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return Response({"message": f"{user.username}'s password updated successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class AllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        return Response(UserSerializer(users, many=True).data)


class PendingBidsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        bids = Bid.objects.filter(status='pending').select_related('user')
        return Response([
            {
                "id": b.id,
                "username": b.user.username,
                "amount": b.amount,
                "plan": b.plan,
                "created": b.created_at,
                "status":b.status
            } for b in bids
        ])


class MarkWithdrawalPaidView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, withdrawal_id):
        try:
            withdrawal = WithdrawalRequest.objects.get(id=withdrawal_id, status='pending')
            withdrawal.status = 'paid'
            withdrawal.save()
            return Response({'message': f'Withdrawal #{withdrawal_id} marked as paid.'})
        except WithdrawalRequest.DoesNotExist:
            return Response({'error': 'Withdrawal not found or already processed.'}, status=404)


class ManualMergeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        bid_ids = request.data.get("bid_ids", [])
        if not bid_ids:
            return Response({"error": "No bid IDs provided."}, status=400)

        bids = Bid.objects.filter(id__in=bid_ids, status='pending', user__in_auction_room=True)
        if not bids.exists():
            return Response({"error": "No valid pending bids found."}, status=400)

        now = timezone.now()
        merged_count = 0

        for bid in bids:
            bid.status = "merged"
            bid.merged_at = now
            bid.save()
            merged_count += 1

        return Response({"message": f"{merged_count} bid(s) merged manually."})


class UpdateMergeSettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = MergeSettings.objects.last()
        return Response({
            "morning_time": settings.morning_time.strftime('%H:%M') if settings else None,
            "evening_time": settings.evening_time.strftime('%H:%M') if settings else None,
        })

    def patch(self, request):
        settings = MergeSettings.objects.last()
        if not settings:
            return Response({"error": "Merge settings not found."}, status=404)

        if "morning_time" in request.data:
            settings.morning_time = request.data["morning_time"]
        if "evening_time" in request.data:
            settings.evening_time = request.data["evening_time"]
        settings.save()

        return Response({"message": "Merge settings updated."})


class CreateInvestmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        amount = request.data.get("amount")
        plan = request.data.get("plan")

        if not all([email, amount, plan]):
            return Response({"error": "Email, amount, and plan are required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        try:
            percent = int(plan.split("_")[0])
        except (ValueError, IndexError):
            return Response({"error": "Invalid plan format."}, status=400)

        expected_return = float(amount) + (float(amount) * percent / 100)

        # Create investment bid and mark as merged immediately
        now = timezone.now()
        bid = Bid.objects.create(
            user=user,
            amount=amount,
            plan=plan,
            expected_return=expected_return,
            type="investment",
            status="merged",           # Immediately running
            merged_at=now              # Mark merged now
        )

        # You can trigger any post-merge logic here if necessary
        # For example: merge_new_investment(bid) - but probably not needed

        return Response({
            "message": f"Investment of ₦{amount} created and running immediately for {user.username}.",
            "bid_id": bid.id,
            "merged": True
        })


class CancelInvestmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        bid_id = request.data.get("bid_id")
        if not bid_id:
            return Response({"error": "Bid ID is required."}, status=400)

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
