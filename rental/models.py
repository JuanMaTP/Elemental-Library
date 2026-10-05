from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from books.models import BookUnit
from general.constants import Type
from person.models import Person


class Rental(models.Model):
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)

    book_unit = models.ForeignKey(BookUnit, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    person_type = models.CharField(max_length=Type.TYPE_CHAR_LENGTH, choices=Type.TYPE_CHOICES, default=Type.STUDENT)

    def __str__(self):
        return f'{self.book_unit} rented by {self.person}'


# Keep BookUnit.borrowed in step with the rental: borrowed while the rental is open,
# available again once it has a return date.
@receiver(post_save, sender=Rental)
def update_book_borrowed(sender, instance, **kwargs):
    BookUnit.objects.filter(pk=instance.book_unit_id).update(borrowed=instance.return_date is None)


@receiver(post_delete, sender=Rental)
def rental_deleted(sender, instance, **kwargs):
    BookUnit.objects.filter(pk=instance.book_unit_id).update(borrowed=False)
