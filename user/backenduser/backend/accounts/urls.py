from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, VerifyEmailOTPView,UserProfileView,enter_auction_room,ResendEmailOTP
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('enter-auction/', enter_auction_room, name='enter-auction-room'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('resend-email-otp/', ResendEmailOTP.as_view(), name='resend-email-otp'),
]