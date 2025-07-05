from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    BidViewSet,
    UploadProofView,
    ConfirmReceiverView,
    WithdrawBidView,
    auto_block,
    run_auto_merge,
    mark_bid_awaiting
)

# DRF router for standard bid CRUD
router = DefaultRouter()
router.register(r'', BidViewSet, basename='bids')

urlpatterns = [
    # Upload proof
    path('upload-proof/<int:pk>/', UploadProofView.as_view(), name='upload-proof'),

    # Confirm receiver has received payment
    path('confirm-receive/<int:bid_id>/', ConfirmReceiverView.as_view(), name='confirm-receive'),

    path('complete-paid-bids/', views.complete_paid_bids, name='complete-paid-bids'),
    path('bids/mark-awaiting/', mark_bid_awaiting),

    # Withdraw to wallet (P2P)
    path('withdraw/', WithdrawBidView.as_view(), name='withdraw-bid'),

    # Cron endpoints for auto merge and auto block
    path('cron/merge/', run_auto_merge, name='cron-auto-merge'),
    path('cron/block/', auto_block, name='cron-auto-block'),
]

# Add router-generated routes
urlpatterns += router.urls
