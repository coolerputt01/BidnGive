from rest_framework import serializers
from .models import ReactivationRequest

class ReactivationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactivationRequest
        fields = ['id', 'proof', 'approved', 'created_at']
        read_only_fields = ['approved', 'created_at']
