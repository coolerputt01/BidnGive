from django.urls import path
from .views import PendingBidsView, ManualMergeView,AuctionStatusView , MarkWithdrawalPaidView,UpdateMergeSettingsView,CreateInvestmentView,CancelInvestmentView, BlockUserView,UnblockUserView,LoginAsUserView,AllUsersView

urlpatterns = [
    path("pending-bids/", PendingBidsView.as_view(), name="pending-bids"),
    path("merge/manual/", ManualMergeView.as_view(), name="manual-merge"),
    path("auction/status/", AuctionStatusView.as_view(), name="auction-status"),
    path('withdrawals/mark-paid/<int:withdrawal_id>/', MarkWithdrawalPaidView.as_view(), name='mark-withdrawal-paid'),
    path("merge/settings/", UpdateMergeSettingsView.as_view(), name="merge-settings"),
    path("create-investment/", CreateInvestmentView.as_view(), name="create-investment"),
    path("cancel-investment/", CancelInvestmentView.as_view(), name="cancel-investment"),
    path("user/block/", BlockUserView.as_view(), name="block-user"),
    path("user/unblock/", UnblockUserView.as_view(), name="unblock-user"),
    path("user/login-as/", LoginAsUserView.as_view(), name="login-as-user"),
    path("admin/all-users/", AllUsersView.as_view(), name="all-users"),
]