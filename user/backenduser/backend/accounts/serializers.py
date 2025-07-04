from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
import random

User = get_user_model()

def generate_otp():
    return str(random.randint(1000, 9999))

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'referral_code',
            'account_number',
            'account_name',
            'bank_name',
            'is_phone_verified',
            'is_email_verified',
            'is_staff',
            'is_disabled',
            'is_active'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = User(**validated_data)
        user.email_otp = generate_otp()
        user.save()
        print(f"Generated OTP for {user.email}: {user.email_otp}")
        if referral_code:
            try:
                user.referred_by = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                pass
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    