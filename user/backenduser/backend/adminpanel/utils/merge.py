from bids.models import Bid
from datetime import datetime
from django.utils.timezone import now

def auto_merge():
    pending_bids = Bid.objects.filter(status='pending').order_by('created_at')
    if pending_bids.count() < 2:
        return "Not enough bids to merge."

    merged_count = 0
    while pending_bids.count() >= 2:
        bid1 = pending_bids[0]
        bid2 = pending_bids[1]

        bid1.status = 'merged'
        bid2.status = 'merged'
        bid1.merged_at = now()
        bid2.merged_at = now()
        bid1.save()
        bid2.save()
        pending_bids = pending_bids[2:]
        merged_count += 2

    return f"{merged_count} bids merged."