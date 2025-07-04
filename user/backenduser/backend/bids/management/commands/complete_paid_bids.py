# bids/management/commands/complete_paid_bids.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bids.models import Bid

class Command(BaseCommand):
    help = 'Automatically mark paid bids as completed after 24 hours'

    def handle(self, *args, **kwargs):
        cutoff_time = timezone.now() - timedelta(hours=24)
        bids = Bid.objects.filter(status='paid', paid_at__lte=cutoff_time)

        count = 0
        for bid in bids:
            bid.status = 'completed'
            bid.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} bid(s) marked as completed.'))
