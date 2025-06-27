from rest_framework.routers import DefaultRouter
from .views import BidViewSet 
from .views import UploadProofView, ConfirmReceiverView
from django.urls import path

router = DefaultRouter()
router.register(r'', BidViewSet, basename='bid')  # register at root

urlpatterns = [
    path('upload-proof/<int:pk>/', UploadProofView.as_view(), name='upload-proof'),
    path('confirm-receive/<int:bid_id>/', ConfirmReceiverView.as_view(), name='confirm-receive'),
]

urlpatterns += router.urls
