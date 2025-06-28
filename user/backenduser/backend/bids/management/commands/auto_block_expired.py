from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from bids.models import Bid
from accounts.utils.send_email import send_ban_notification

class Command(BaseCommand):
    help = 'Block users with expired merged bids (no proof within 5 hours).'

    def handle(self, *args, **options):
        expiration_cutoff = now() - timedelta(hours=5)
        expired_bids = Bid.objects.filter(
            status='merged',
            merged_at__lt=expiration_cutoff,
            payment_proof__isnull=True
        )

        if not expired_bids.exists():
            self.stdout.write("✅ No expired bids found.")
            return

        blocked_count = 0

        for bid in expired_bids:
            user = bid.user
            if user and user.is_active:
                # Send ban email and block
                send_ban_notification(user.email)
                user.is_active = False
                user.save()

            bid.status = 'expired'
            bid.save()
            blocked_count += 1
            self.stdout.write(f"⛔ User {user.username} blocked for Bid #{bid.id}")

        self.stdout.write(f"\n✅ Done. {blocked_count} user(s) blocked for bid expiry.")
