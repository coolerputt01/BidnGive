from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, VerifyEmailOTPView,SendWhatsAppOTP,verify_whatsapp_otp,UserProfileView,enter_auction_room
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify-email'),
    path('send-whatsapp-otp/', SendWhatsAppOTP.as_view()),
    path('verify-whatsapp-otp/', verify_whatsapp_otp),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('enter-auction/', enter_auction_room, name='enter-auction-room'),
    path('api/admin/token/', CustomTokenObtainPairView.as_view(), name='admin_token_obtain_pair'),
]