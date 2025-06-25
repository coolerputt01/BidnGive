from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    account_number = models.CharField(max_length=11,unique=True, null=True,blank=True)
    is_disabled = models.BooleanField(default=False)
    last_login_bonus = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    phone_otp = models.CharField(max_length=6, null=True, blank=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = f"REF{self.username[:3].upper()}{self.id or ''}"
        super().save(*args, **kwargs)
