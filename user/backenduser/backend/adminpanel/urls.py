from django.urls import path
from .views import PendingBidsView, ReferralBonusRequestsView, ManualMergeView,AuctionStatusView

urlpatterns = [
    path("pending-bids/", PendingBidsView.as_view(), name="pending-bids"),
    path("referral-requests/", ReferralBonusRequestsView.as_view(), name="referral-requests"),
    path("merge/manual/", ManualMergeView.as_view(), name="manual-merge"),
    path("auction/status/", AuctionStatusView.as_view(), name="auction-status"),
]