from .models import Referral, ReferralBonus
from wallet.models import Wallet, WalletTransaction
from decimal import Decimal

def award_referral_bonus(bid):
    user = bid.user
    bid_id = bid.id
    amount = bid.amount

    # Only apply to the user's first paid investment
    if user.bids.filter(status='paid', type='investment').count() > 1:
        return

    try:
        referral = Referral.objects.get(referred=user)
        first_level = referral.referrer

        # 5% bonus for direct referrer
        first_bonus = ReferralBonus.objects.create(
            user=first_level,
            amount=Decimal(amount) * Decimal('0.05'),
            level=1,
            bid_id=bid_id
        )

        wallet1, _ = Wallet.objects.get_or_create(user=first_level)
        wallet1.balance += first_bonus.amount
        wallet1.save()

        WalletTransaction.objects.create(
            user=first_level,
            wallet=wallet1,
            amount=first_bonus.amount,
            type='credit',
            description='Referral bonus (level 1)'
        )

        # Check for second-level referrer
        second_ref = Referral.objects.filter(referred=first_level).first()
        if second_ref:
            second_level = second_ref.referrer

            second_bonus = ReferralBonus.objects.create(
                user=second_level,
                amount=Decimal(amount) * Decimal('0.02'),
                level=2,
                bid_id=bid_id
            )

            wallet2, _ = Wallet.objects.get_or_create(user=second_level)
            wallet2.balance += second_bonus.amount
            wallet2.save()

            WalletTransaction.objects.create(
                user=second_level,
                wallet=wallet2,
                amount=second_bonus.amount,
                type='credit',
                description='Referral bonus (level 2)'
            )

    except Referral.DoesNotExist:
        pass  # No referrer, no bonus
