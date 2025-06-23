from django.db import models
from django.conf import settings

class Referral(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='referrals_made', on_delete=models.CASCADE)
    referred = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='referral', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReferralBonus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.PositiveIntegerField(default=1)  # 1 for direct, 2 for 2nd-level
    bid_id = models.PositiveIntegerField()  # Link to the original bid
    created_at = models.DateTimeField(auto_now_add=True)
    withdrawn = models.BooleanField(default=False)
