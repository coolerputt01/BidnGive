from django.db import models
from django.conf import settings

class ReactivationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proof = models.ImageField(upload_to='reactivation_proofs/')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
