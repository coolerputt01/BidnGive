from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Bid(models.Model):
    PLAN_CHOICES = [
        ('50_24', '50% in 24 hours'),
    ]

    TYPE_CHOICES = [
        ('investment', 'Investment'),
        ('withdrawal', 'Withdrawal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('merged', 'Merged'),
        ('paid', 'Paid'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='investment')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    merged_bid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='merged_bids')
    merged_at = models.DateTimeField(null=True, blank=True)

    payment_proof = models.ImageField(upload_to='proofs/', null=True, blank=True)
    sender_confirmed = models.BooleanField(default=False)
    receiver_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    can_recommit = models.BooleanField(default=False)

    paid_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return self.status == 'merged' and self.merged_at and timezone.now() > self.merged_at + timezone.timedelta(hours=5)

    def expected_profit(self):
        return self.expected_return - self.amount

    def __str__(self):
        return f"Bid #{self.id} by {self.user.username} - {self.amount} ({self.status})"

    def get_counterparty_bid(self):
        if self.merged_bid:
            return self.merged_bid
        return Bid.objects.filter(merged_bid=self).first()

    def get_counterparty(self):
        bid = self.get_counterparty_bid()
        return bid.user if bid else None
