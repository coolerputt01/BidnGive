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
from django.utils.timezone import localtime, make_aware, now as dj_now

class AuctionStatusView(APIView):
    def get(self, request):
        now = localtime(dj_now())
        today = now.date()

        settings = MergeSettings.objects.last()
        if not settings:
            return Response({"error": "Merge settings not found."}, status=404)

        # Only morning and evening now
        times = [
            settings.morning_time,
            settings.evening_time
        ]
        auction_duration = timedelta(minutes=settings.auction_duration_minutes)

        status = "closed"
        next_auction = None

        for auction_time in sorted(times):
            auction_dt = localtime(make_aware(datetime.combine(today, auction_time)))
            if auction_dt <= now < auction_dt + auction_duration:
                status = "open"
                next_auction = auction_dt
                break
            if now < auction_dt and (not next_auction or auction_dt < next_auction):
                next_auction = auction_dt

        if not next_auction:
            next_auction = localtime(make_aware(
                datetime.combine(today + timedelta(days=1), settings.morning_time)
            ))

        remaining_seconds = int((next_auction - now).total_seconds())

        return Response({
            "market_status": status,
            "next_auction": next_auction.isoformat(),
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
        bids = Bid.objects.all().select_related('user')
        return Response([
            {
                "id": b.id,
                "username": b.user.username,
                "amount": b.amount,
                "plan": b.plan,
                "created": b.created_at,
                "status":b.status,
                "type":b.type,
                "admin_paid":b.admin_paid
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

        bids = list(Bid.objects.filter(id__in=bid_ids, status='awaiting'))

        if len(bids) < 2 or len(bids) % 2 != 0:
            return Response({"error": "You must select an even number of bids to merge in pairs."}, status=400)

        now = timezone.now()
        merged_count = 0

        # Merge in pairs
        for i in range(0, len(bids), 2):
            bid1 = bids[i]
            bid2 = bids[i + 1]

            # Decide roles: First one is buyer, second is seller
            bid1.status = 'merged'
            bid1.merged_at = now
            bid1.bid_role = 'buyer'
            bid1.type = 'investment'
            bid1.merged_bid = bid2

            bid2.status = 'merged'
            bid2.merged_at = now
            bid2.bid_role = 'seller'
            bid2.type = 'withdrawal'
            bid2.merged_bid = bid1

            bid1.save()
            bid2.save()
            merged_count += 2

        return Response({"message": f"{merged_count} bid(s) merged manually."})

class UpdateMergeSettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = MergeSettings.objects.last()
        if not settings:
            return Response({}, status=404)
        return Response({
            "morning_time": settings.morning_time.strftime('%H:%M'),
            "evening_time": settings.evening_time.strftime('%H:%M'),
            "auction_duration_minutes": settings.auction_duration_minutes
        })

    def patch(self, request):
        settings = MergeSettings.objects.last()
        if not settings:
            return Response({"error": "Merge settings not found."}, status=404)

        if "morning_time" in request.data:
            settings.morning_time = request.data["morning_time"]
        if "evening_time" in request.data:
            settings.evening_time = request.data["evening_time"]
        if "auction_duration_minutes" in request.data:
            settings.auction_duration_minutes = int(request.data["auction_duration_minutes"])

        settings.save()
        return Response({"message": "Merge settings updated."})

class CreateInvestmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")
        amount = request.data.get("amount")
        plan = request.data.get("plan")
        type_of = request.data.get("type")
        counterparty_email = request.data.get("counterparty_email")

        if not all([email, amount, plan, type_of]):
            return Response({"error": "Email, amount, plan, and type are required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        try:
            percent = int(plan.split("_")[0])
        except (ValueError, IndexError):
            return Response({"error": "Invalid plan format."}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Amount must be a number."}, status=400)

        expected_return = amount + (amount * percent / 100)
        now = timezone.now()

        # Handle counterparty logic
        counterparty_bid = None
        if counterparty_email:
            try:
                counterparty_user = User.objects.get(email=counterparty_email)
            except User.DoesNotExist:
                return Response({"error": "Counterparty user not found."}, status=404)

            counterparty_bid = Bid.objects.filter(
                user=counterparty_user,
                status='awaiting',
                merged_bid__isnull=True
            ).first()

            if not counterparty_bid:
                return Response({"error": "No available bid found for counterparty user."}, status=400)

        # Create the admin-side bid
        bid = Bid.objects.create(
            user=user,
            amount=amount,
            plan=plan,
            expected_return=expected_return,
            type=type_of,  # initial type; will update if merged
            status='merged' if counterparty_bid else 'awaiting',
            merged_bid=counterparty_bid if counterparty_bid else None,
            merged_at=now if counterparty_bid else None,
            admin_paid=True,
            role=None  # will set later if merged
        )

        # If a counterparty is found, finalize linking and roles
        if counterparty_bid:
            # Update counterparty bid
            counterparty_bid.merged_bid = bid
            counterparty_bid.status = 'merged'
            counterparty_bid.merged_at = now
            counterparty_bid.role = 'seller'
            counterparty_bid.type = 'withdrawal'
            counterparty_bid.save()

            # Update admin-created bid
            bid.role = 'buyer'
            bid.type = 'investment'
            bid.save()

        return Response({
            "message": f"Investment of ₦{amount} created for {user.username} and merged with counterparty." if counterparty_bid else f"Investment of ₦{amount} created and running.",
            "bid_id": bid.id,
            "merged": bool(counterparty_bid),
            "counterparty_email": counterparty_email if counterparty_bid else None
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
