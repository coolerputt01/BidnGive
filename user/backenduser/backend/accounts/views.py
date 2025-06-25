from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from accounts.utils.send_whatsapp import send_whatsapp
import random

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # 👈 enables email login

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['is_phone_verified'] = self.user.is_phone_verified
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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

class SendWhatsAppOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp = str(random.randint(100000, 999999))
        user.phone_otp = otp
        user.save()

        send_whatsapp(
            phone=user.phone_number,
            message=f"Your BID 'N' GIVE WhatsApp OTP is *{otp}*"
        )
        return Response({'message': 'OTP sent to your WhatsApp successfully.'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_whatsapp_otp(request):
    otp = request.data.get('otp')
    user = request.user

    if user.phone_otp == otp:
        user.phone_verified = True
        user.phone_otp = None
        user.save()
        return Response({'message': 'Phone verified successfully'})
    return Response({'error': 'Invalid OTP'}, status=400)
