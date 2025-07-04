from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer , generate_otp
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from accounts.utils.send_email import send_otp_email
from bids.models import Bid
from django.conf import settings
import random

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # Send email OTP
        send_otp_email(user.email, user.email_otp)

class ResendEmailOTP(APIView):
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        try:
            user = User.objects.get(email=email)
            if user.is_email_verified:
                return Response({"message": "Email already verified."})
            otp = generate_otp()
            user.email_otp = otp
            user.save()
            send_otp_email(email, otp)
            return Response({"message": "OTP resent to email."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid email or password.')
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        # Admin route check
        if request.path.startswith('/api/admin/'):
            if email != settings.ADMIN_EMAIL or password != settings.ADMIN_PASSWORD:
                raise serializers.ValidationError('You are not authorized to log in as admin.')

        self.user = user

        data = super().validate(attrs)
        data['user_id'] = user.id
        data['username'] = user.username
        data['is_staff'] = user.is_staff
        data['is_phone_verified'] = user.is_phone_verified
        data['is_email_verified'] = user.is_email_verified
        data['is_active'] = user.is_active
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ReferralDownlinesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        downlines = User.objects.filter(referred_by=request.user)
        return Response(UserSerializer(downlines, many=True).data)

class VerifyEmailOTPView(APIView):
    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        otp = request.data.get("otp", "").strip()

        if not email or not otp:
            return Response({"error": "Both email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.email_otp != otp:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP matched

        user.is_email_verified = True
        user.email_otp = None
        user.save()
        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enter_auction_room(request):
    user = request.user

    # Check if the user has pending bids
    has_pending = Bid.objects.filter(user=user, status='pending').exists()

    if not has_pending:
        return Response({"message": "You must have at least one pending bid to join the auction room."}, status=400)

    # Update user status
    user.in_auction_room = True
    user.save()

    return Response({"message": "You have entered the auction room."})

