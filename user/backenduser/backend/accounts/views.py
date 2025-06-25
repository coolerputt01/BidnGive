from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from .models import User
from utils.send_whatsapp import send_whatsapp
import random

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['is_phone_verified'] = self.user.is_phone_verified
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class VerifyEmailOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_email_verified = True
                user.otp = None  # clear used OTP
                user.save()
                return Response({"message": "Email verified successfully"})
            return Response({"error": "Invalid OTP"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

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
