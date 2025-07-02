from django.db import transaction
from django.utils.timezone import now
from bids.models import Bid
from decimal import Decimal



def merge_new_investment(investment_bid):
    """
    Try to merge a newly created investment bid with any matching withdrawal bid(s).
    Returns True if merge was successful.
    """
    if investment_bid.status != 'pending' or investment_bid.type != 'investment':
        return False

    sellers = list(Bid.objects.filter(status='pending', type='withdrawal').order_by('amount'))

    for seller in sellers:
        if investment_bid.amount == seller.amount:
            with transaction.atomic():
                investment_bid.status = 'merged'
                investment_bid.merged_bid = seller
                investment_bid.merged_at = now()
                investment_bid.save()

                seller.status = 'merged'
                seller.merged_bid = investment_bid
                seller.merged_at = now()
                seller.save()
                return True

    return False  # no match found
