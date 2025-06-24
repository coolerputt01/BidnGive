from django.urls import path
from .views import PendingBidsView, ManualMergeView,AuctionStatusView ,  PendingWithdrawalsView, MarkWithdrawalPaidView

urlpatterns = [
    path("pending-bids/", PendingBidsView.as_view(), name="pending-bids"),
    path("merge/manual/", ManualMergeView.as_view(), name="manual-merge"),
    path("auction/status/", AuctionStatusView.as_view(), name="auction-status"),
    path('withdrawals/pending/', PendingWithdrawalsView.as_view(), name='pending-withdrawals'),
    path('withdrawals/mark-paid/<int:withdrawal_id>/', MarkWithdrawalPaidView.as_view(), name='mark-withdrawal-paid'),
]