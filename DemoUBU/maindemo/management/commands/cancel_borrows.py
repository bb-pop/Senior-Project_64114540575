from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from maindemo.models import BorrowRecord

class Command(BaseCommand):
    help = 'Cancel borrow records that are older than 10 minutes and still in "waiting" status.'

    def handle(self, *args, **options):
        now = timezone.now()
        ten_minutes_ago = now - timedelta(minutes=10)
        records_to_cancel = BorrowRecord.objects.filter(status='waiting', borrow_date__lte=ten_minutes_ago)

        count = 0
        for record in records_to_cancel:
            record.status = 'cancel'
            record.save()
            record.item.quantity += record.quantity
            record.item.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Cancelled {count} borrow records.'))
