from django.core.management.base import BaseCommand
from django.utils.timezone import now
from bids.models import Bid
from django.db import transaction
from decimal import Decimal

class Command(BaseCommand):
    help = 'Merge sellers (withdrawal) with buyers (investment) based on amount.'

    def handle(self, *args, **options):
        buyers = list(Bid.objects.filter(status='pending', type='investment').order_by('-amount'))  # big buyers first
        sellers = list(Bid.objects.filter(status='pending', type='withdrawal').order_by('amount'))  # small sellers first

        used_buyers = set()
        used_sellers = set()
        merged_count = 0

        for seller in sellers:
            if seller.id in used_sellers:
                continue

            # Try to find one buyer with equal amount
            for buyer in buyers:
                if buyer.id in used_buyers:
                    continue
                if buyer.amount == seller.amount:
                    self.merge_pair(buyer, seller)
                    used_buyers.add(buyer.id)
                    used_sellers.add(seller.id)
                    merged_count += 2
                    break
            else:
                # Try to combine multiple buyers to match seller amount
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

                if total == seller.amount and match_buyers:
                    with transaction.atomic():
                        for buyer in match_buyers:
                            buyer.status = 'merged'
                            buyer.merged_bid = seller
                            buyer.merged_at = now()
                            buyer.save()
                            used_buyers.add(buyer.id)

                        seller.status = 'merged'
                        seller.merged_at = now()
                        seller.merged_bid = match_buyers[0]  # optional: just assign one
                        seller.save()
                        used_sellers.add(seller.id)
                        merged_count += len(match_buyers) + 1

        if merged_count:
            self.stdout.write(self.style.SUCCESS(f"✅ {merged_count} bids merged successfully."))
        else:
            self.stdout.write("❌ No matching buyer-seller pairs found.")

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
