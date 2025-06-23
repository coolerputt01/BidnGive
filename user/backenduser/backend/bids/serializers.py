from rest_framework import serializers
from .models import Bid
from decimal import Decimal

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['user', 'status', 'merged_with', 'merged_at','expected_return']

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        plan = validated_data['plan']
        expected_return = 0
        if plan == '50_24':
            expected_return = amount * Decimal('1.5')
        return Bid.objects.create(user=user, amount=amount, plan=plan, expected_return=expected_return)
    
class BidPaymentConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'payment_proof', 'sender_confirmed', 'receiver_confirmed']
        read_only_fields = ['sender_confirmed', 'receiver_confirmed']

    def update(self, instance, validated_data):
        request = self.context['request']
        if 'payment_proof' in validated_data:
            instance.payment_proof = validated_data['payment_proof']
            instance.sender_confirmed = True
        instance.save()
        return instance