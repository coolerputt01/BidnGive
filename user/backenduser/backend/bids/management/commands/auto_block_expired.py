from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from bids.models import Bid
from accounts.utils.send_email import send_ban_notification
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Block users with expired merged bids (no proof within 5 hours).'

    def handle(self, *args, **options):
        expiration_cutoff = now() - timedelta(hours=5)
        expired_bids = Bid.objects.select_related('user').filter(
            status='merged',
            merged_at__lt=expiration_cutoff,
            payment_proof__isnull=True
        )

        if not expired_bids.exists():
            logger.info("✅ No expired bids found.")
            return

        blocked_count = 0

        for bid in expired_bids:
            user = bid.user

            if not user:
                logger.warning(f"⚠️ Bid #{bid.id} has no associated user.")
                continue

            if user.is_active:
                # Send ban email and deactivate user
                send_ban_notification(user.email)
                user.is_disabled = False
                user.save()
                logger.info(f"⛔ User {user.username} blocked due to Bid #{bid.id}")

            # Expire the bid
            bid.status = 'expired'
            bid.save()
            blocked_count += 1

        logger.info(f"\n✅ Done. {blocked_count} user(s) blocked for bid expiry.")
