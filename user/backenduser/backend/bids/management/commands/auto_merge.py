from django.core.management.base import BaseCommand
from bids.models import Bid
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Automatically merge pending bids into user pairs (different users only).'

    def handle(self, *args, **kwargs):
        pending_bids = list(Bid.objects.filter(status='pending').order_by('created_at'))

        if len(pending_bids) < 2:
            self.stdout.write("Not enough bids to merge.")
            return

        merged_count = 0
        used_ids = set()

        for i in range(len(pending_bids)):
            bid1 = pending_bids[i]
            if bid1.id in used_ids:
                continue

            for j in range(i + 1, len(pending_bids)):
                bid2 = pending_bids[j]
                if bid2.id in used_ids or bid1.user == bid2.user:
                    continue

                # Mark both as merged
                bid1.status = bid2.status = 'merged'
                bid1.merged_at = bid2.merged_at = now()

                # Set merged_with field
                bid1.merged_with = bid2.user
                bid2.merged_with = bid1.user

                # Optional: set bank details for bid2 to pay bid1
                bid2.receiver_account = bid1.user.account_number
                bid2.receiver_bank = bid1.user.referred_by  # or any bank field you use
                bid2.receiver_phone = bid1.user.phone_number

                bid1.save()
                bid2.save()

                used_ids.update([bid1.id, bid2.id])
                merged_count += 2
                break  # proceed to the next available bid

        if merged_count == 0:
            self.stdout.write("No valid user pairs to merge.")
        else:
            self.stdout.write(self.style.SUCCESS(f"{merged_count} bids merged successfully."))
