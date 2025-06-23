from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_bonus_date = models.DateField(null=True, blank=True)

    def credit(self, amount):
        self.balance += amount
        self.save()