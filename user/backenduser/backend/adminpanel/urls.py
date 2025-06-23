from django.urls import path
from .views import PendingBidsView, ReferralBonusRequestsView, ManualMergeView

urlpatterns = [
    path("pending-bids/", PendingBidsView.as_view(), name="pending-bids"),
    path("referral-requests/", ReferralBonusRequestsView.as_view(), name="referral-requests"),
    path("merge/manual/", ManualMergeView.as_view(), name="manual-merge"),
]