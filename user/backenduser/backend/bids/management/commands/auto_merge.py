from django.core.management.base import BaseCommand
from django.utils.timezone import now
from bids.models import Bid
from django.db import transaction

class Command(BaseCommand):
    help = 'Automatically merge eligible pending bids into pairs (must be different users).'

    def handle(self, *args, **options):
        pending_bids = list(Bid.objects.filter(status='pending').order_by('created_at'))

        if len(pending_bids) < 2:
            self.stdout.write("⚠️ Not enough bids to merge.")
            return

        used = set()
        merged_count = 0

        for i in range(len(pending_bids)):
            bid1 = pending_bids[i]
            if bid1.id in used:
                continue

            for j in range(i + 1, len(pending_bids)):
                bid2 = pending_bids[j]
                if bid2.id in used or bid1.user == bid2.user:
                    continue

                with transaction.atomic():
                    # Merge logic
                    bid1.status = bid2.status = 'merged'
                    bid1.merged_at = bid2.merged_at = now()
                    bid1.merged_with = bid2.user
                    bid2.merged_with = bid1.user

                    # Set receiver (bid1 is receiving, bid2 is sending)
                    bid2.receiver_account = bid1.user.account_number
                    # bid2.receiver_bank = bid1.user.bank_name  ← Removed this line
                    bid2.receiver_phone = bid1.user.phone_number

                    bid1.save()
                    bid2.save()

                used.update([bid1.id, bid2.id])
                merged_count += 2
                break  # Move to next available bid

        if merged_count:
            self.stdout.write(self.style.SUCCESS(f"✅ {merged_count} bids merged successfully."))
        else:
            self.stdout.write("❌ No valid user pairs found to merge.")
