from celery import shared_task
from django.conf import settings
from django.utils import timezone

from rental.models import Rental


@shared_task
def check_rentals_return():
    """
    Return every rental that has been open for longer than RENTAL_PERIOD.
    Saving each rental sets its return date and makes the book unit available again.
    """
    now = timezone.now()
    overdue = Rental.objects.filter(return_date__isnull=True, rental_date__lt=now - settings.RENTAL_PERIOD)

    returned = 0
    for rental in overdue:
        rental.return_date = now
        rental.save()
        returned += 1

    return returned
