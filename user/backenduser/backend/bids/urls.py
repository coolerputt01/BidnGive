from rest_framework.routers import DefaultRouter
from .views import BidViewSet , enter_auction_room
from .views import UploadProofView, ConfirmReceiverView
from django.urls import path

router = DefaultRouter()
router.register(r'', BidViewSet, basename='bid')

urlpatterns = router.urls

urlpatterns += [
    path('upload-proof/<int:pk>/', UploadProofView.as_view(), name='upload-proof'),
    path('confirm-receive/<int:bid_id>/', ConfirmReceiverView.as_view(), name='confirm-receive'),
    path('enter-auction/', enter_auction_room, name='enter-auction-room'),
]
