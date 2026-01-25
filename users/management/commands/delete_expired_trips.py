from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import HostTrip

class Command(BaseCommand):
    help = 'Delete host trips that are 24 hours past their departure date'

    def handle(self, *args, **options):
        # Calculate the cutoff date: 24 hours ago
        cutoff_datetime = timezone.now() - timedelta(hours=24)

        # Filter trips where departure_date + 1 day is before now
        expired_trips = HostTrip.objects.filter(
            departure_date__lt=cutoff_datetime.date()
        )

        count = expired_trips.count()
        if count > 0:
            expired_trips.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {count} expired host trip(s).')
            )
        else:
            self.stdout.write('No expired host trips found.')
