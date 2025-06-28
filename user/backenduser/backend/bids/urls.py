from rest_framework.routers import DefaultRouter
from .views import BidViewSet 
from .views import UploadProofView, ConfirmReceiverView,run_auto_merge, auto_block, WithdrawBidView
from django.urls import path

router = DefaultRouter()
router.register(r'', BidViewSet, basename='bid')  # register at root

urlpatterns = [
    path('upload-proof/<int:pk>/', UploadProofView.as_view(), name='upload-proof'),
    path('confirm-receive/<int:bid_id>/', ConfirmReceiverView.as_view(), name='confirm-receive'),
    path('withdraw-bid/', WithdrawBidView.as_view(), name='withdraw-bid'),
    path('api/cron/merge/', run_auto_merge),
    path('api/cron/bonus/', auto_block),
]

urlpatterns += router.urls
