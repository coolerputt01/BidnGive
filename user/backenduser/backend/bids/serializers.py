from rest_framework import serializers
from .models import Bid
from decimal import Decimal

class BidSerializer(serializers.ModelSerializer):
    payment_proof = serializers.SerializerMethodField()
    counterparties = serializers.SerializerMethodField()
    can_recommit = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = [
            'id', 'user', 'amount', 'plan', 'expected_return', 'type', 'status',
            'merged_bid', 'merged_at', 'payment_proof', 'sender_confirmed', 'receiver_confirmed',
            'created_at', 'can_recommit', 'paid_at', 'admin_paid', 'counterparties', 'role'
        ]

    def get_payment_proof(self, obj):
        if obj.payment_proof:
            return obj.payment_proof.url  # Cloudinary auto-generates the full URL
        return None

    def get_role(self, obj):
        return 'seller' if obj.type == 'withdrawal' else 'buyer'

    def get_can_recommit(self, obj):
        user = obj.user
        return Bid.objects.filter(user=user, status='paid').exclude(id=obj.id).exists()

    def get_counterparties(self, obj):
        if not obj.merged_bid:
            merged_bids = Bid.objects.filter(merged_bid=obj).exclude(id=obj.id)
        else:
            merged_bids = [obj.merged_bid]

        result = []
        for bid in merged_bids:
            user = bid.user
            result.append({
                "username": user.username,
                "phone_number": user.phone_number,
                "account_number": getattr(user, 'account_number', ''),
                "account_name": getattr(user, 'account_name', ''),
                "bank_name": getattr(user, 'bank_name', ''),
                "role": 'seller' if bid.type == 'withdrawal' else 'buyer'
            })
        return result

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



# bids/serializers.py
class PaymentProofSerializer(serializers.ModelSerializer):
    payment_proof = serializers.ImageField(required=True)

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
            raise serializers.ValidationError("Bid is not marked as paid yet.")

        attrs['bid'] = bid
        return attrs

    def save(self):
        bid = self.validated_data['bid']
        bid.receiver_confirmed = True
        bid.status = 'confirmed'
        bid.can_recommit = True
        bid.save()
        return bid