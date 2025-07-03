import logging
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from bids.models import Bid
from django.db import transaction
from decimal import Decimal

# Configure logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Merge sellers (withdrawal) with buyers (investment) based on amount, prioritizing multiple buyer combos.'

    def handle(self, *args, **options):
        logger.info("🔄 Starting merge process...")

        buyers = Bid.objects.filter(
            status='pending',
            type='investment',
            user__in_auction_room=True
        ).order_by('amount')  # Start with smaller buyers

        sellers = Bid.objects.filter(
            status='pending',
            type='withdrawal',
            user__in_auction_room=True
        ).order_by('amount')

        used_buyers = set()
        used_sellers = set()
        merged_count = 0

        for seller in sellers:
            if seller.id in used_sellers:
                continue

            # Try to combine multiple buyers
            match_buyers = []
            total = Decimal('0')
            for buyer in buyers:
                if buyer.id in used_buyers:
                    continue
                if total + buyer.amount <= seller.amount:
                    match_buyers.append(buyer)
                    total += buyer.amount
                if total == seller.amount:
                    break

            if total == seller.amount and len(match_buyers) >= 1:
                with transaction.atomic():
                    for buyer in match_buyers:
                        buyer.status = 'merged'
                        buyer.merged_bid = seller
                        buyer.merged_at = now()
                        buyer.save()
                        used_buyers.add(buyer.id)
                        logger.info(f"🔗 Sub-Merged Buyer #{buyer.id} into Seller #{seller.id}")

                    seller.status = 'merged'
                    seller.merged_bid = match_buyers[0]  # optional representative
                    seller.merged_at = now()
                    seller.save()
                    used_sellers.add(seller.id)
                    merged_count += len(match_buyers) + 1
                    logger.info(f"🔗 Seller #{seller.id} merged with {len(match_buyers)} buyers.")
                continue  # Skip 1-to-1 matching if multiple matched

            # Try a last-resort 1-to-1 exact match if combo wasn't possible
            for buyer in buyers:
                if buyer.id in used_buyers:
                    continue
                if buyer.amount == seller.amount:
                    self.merge_pair(buyer, seller)
                    used_buyers.add(buyer.id)
                    used_sellers.add(seller.id)
                    merged_count += 2
                    logger.info(f"🔗 Fallback: Single Buyer #{buyer.id} matched with Seller #{seller.id}")
                    break

        if merged_count:
            logger.success = getattr(logger, "success", logger.info)
            logger.success(f"✅ Total merged: {merged_count} bids.")
        else:
            logger.warning("❌ No matching buyer-seller pairs found.")

    def merge_pair(self, buyer, seller):
        with transaction.atomic():
            buyer.status = 'merged'
            buyer.merged_bid = seller
            buyer.merged_at = now()
            buyer.save()

            seller.status = 'merged'
            seller.merged_bid = buyer
            seller.merged_at = now()
            seller.save()
