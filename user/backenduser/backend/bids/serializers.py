from rest_framework import serializers
from .models import Bid
from decimal import Decimal

class BidSerializer(serializers.ModelSerializer):
    counterparty_name = serializers.SerializerMethodField()
    counterparty_phone = serializers.SerializerMethodField()
    counterparty_account = serializers.SerializerMethodField()
    counterparty_bank = serializers.SerializerMethodField()
    counterparty_role = serializers.SerializerMethodField()  # NEW
    can_recommit = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = [
            'user', 'status', 'expected_return', 'merged_bid',
            'merged_at', 'sender_confirmed', 'receiver_confirmed',
            'can_recommit', 'counterparty_name', 'counterparty_phone',
            'counterparty_account', 'counterparty_bank',
            'role', 'counterparty_role'  # NEW
        ]

    def get_counterparty_name(self, obj):
        pair = obj.get_counterparty()
        return pair.get_full_name() if pair else None

    def get_counterparty_phone(self, obj):
        pair = obj.get_counterparty()
        return pair.phone_number if pair else None

    def get_counterparty_account(self, obj):
        pair = obj.get_counterparty()
        return pair.account_number if pair else None

    def get_counterparty_bank(self, obj):
        pair = obj.get_counterparty()
        return pair.bank_name if pair else None

    def get_role(self, obj):
        return 'seller' if obj.type == 'withdrawal' else 'buyer'

    def get_counterparty_role(self, obj):
        pair = obj.get_counterparty()
        if not pair:
            return None
        bid = pair.bids.filter(merged_bid=obj).first() or pair.bids.filter(id=obj.merged_bid_id).first()
        if bid:
            return 'seller' if bid.type == 'withdrawal' else 'buyer'
        return None

    def get_can_recommit(self, obj):
        user = obj.user
        return Bid.objects.filter(user=user, status='paid').exclude(id=obj.id).exists()

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        plan = validated_data['plan']

        if Bid.objects.filter(user=user).exclude(status='paid').exists():
            raise serializers.ValidationError("You already have an active/pending bid.")

        expected_return = amount * Decimal('1.5') if plan == '50_24' else Decimal('0')

        return Bid.objects.create(
            user=user,
            amount=amount,
            plan=plan,
            expected_return=expected_return
        )


class PaymentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'payment_proof']

    def update(self, instance, validated_data):
        request = self.context['request']
        if instance.status != 'merged':
            raise serializers.ValidationError("You can only upload proof for merged bids.")

        instance.payment_proof = validated_data.get('payment_proof')
        instance.sender_confirmed = True
        instance.status = 'paid'
        instance.save()
        return instance


class ConfirmPaymentSerializer(serializers.Serializer):
    bid_id = serializers.IntegerField()

    def validate(self, attrs):
        bid_id = attrs.get('bid_id')
        request = self.context['request']

        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            raise serializers.ValidationError("Bid not found.")

        if bid.user == request.user:
            raise serializers.ValidationError("You can't confirm your own payment.")

        if bid.status != 'paid':
            raise serializers.ValidationError("Bid is not marked as paid.")

        attrs['bid'] = bid
        return attrs

    def save(self):
        bid = self.validated_data['bid']
        bid.receiver_confirmed = True
        bid.status = 'confirmed'
        bid.can_recommit = True
        bid.save()
        return bid
