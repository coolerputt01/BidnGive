from django.core.management.base import BaseCommand
from utils.merge import auto_merge

class Command(BaseCommand):
    help = 'Run auto merge for bids'

    def handle(self, *args, **kwargs):
        result = auto_merge()
        self.stdout.write(self.style.SUCCESS(result))