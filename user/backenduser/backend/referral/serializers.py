from rest_framework import serializers
from .models import ReferralBonus

class ReferralBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralBonus
        fields = '__all__'