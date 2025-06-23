from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, VerifyEmailOTPView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('verify-email/', VerifyEmailOTPView.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]