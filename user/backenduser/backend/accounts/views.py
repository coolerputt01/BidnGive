from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from .models import User

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