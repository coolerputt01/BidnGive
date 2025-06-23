from django.db import models
from django.conf import settings
from django.utils import timezone

class Bid(models.Model):
    PLAN_CHOICES = [
        ('50_24', '50% in 24 hours'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # pending, merged, paid, confirmed, cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    merged_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='merged_bids')
    merged_at = models.DateTimeField(null=True, blank=True)
    payment_proof = models.ImageField(upload_to='proofs/', null=True, blank=True)
    sender_confirmed = models.BooleanField(default=False)
    receiver_confirmed = models.BooleanField(default=False)
    in_auction_room = models.BooleanField(default=False)

    def is_expired(self):
        if self.status == 'merged' and self.merged_at:
            return timezone.now() > self.merged_at + timezone.timedelta(hours=5)
        return False