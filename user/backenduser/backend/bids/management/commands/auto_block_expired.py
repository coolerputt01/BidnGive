from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from bids.models import Bid

class Command(BaseCommand):
    help = 'Auto-block users whose merged bids expired without payment proof'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_bids = Bid.objects.filter(
            status='merged',
            merged_at__lt=now - timedelta(hours=5),
            payment_proof__isnull=True
        )

        if not expired_bids.exists():
            self.stdout.write("✅ No expired merged bids found.")
            return

        count = 0
        for bid in expired_bids:
            if bid.user:  # ensure user exists
                if bid.user.is_active:
                    bid.user.is_active = False
                    bid.user.save()
                bid.status = 'expired'
                bid.save()
                count += 1
                self.stdout.write(f"⛔ User {bid.user.username} blocked for bid #{bid.id}")
            else:
                self.stdout.write(f"⚠️ Skipped bid #{bid.id} (no user assigned)")

        self.stdout.write(f"\n✅ Done. {count} user(s) blocked.")
