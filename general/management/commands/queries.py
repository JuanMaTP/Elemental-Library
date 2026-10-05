import datetime

from django.core.management import BaseCommand
from django.db.models import Count
from django.utils.timezone import make_aware

from author.models import Author
from books.models import BookUnit
from person.models import Person
from rental.models import Rental


def next_month(date):
    """First day of the month after `date` (handles December)."""
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1, day=1)
    return date.replace(month=date.month + 1, day=1)


class Command(BaseCommand):
    help = 'Example queries over the library data; pick one with --choice 1-7'

    def add_arguments(self, parser):
        parser.add_argument('--choice', type=int)
        parser.add_argument('--book_id', type=int)

    def handle(self, *args, **options):
        choice = options['choice']
        if choice == 1:
            self.authors_over_25()
        elif choice == 2:
            self.book_has_been_borrowed(options['book_id'])
        elif choice == 3:
            self.book_rental_amount_this_month()
        elif choice == 4:
            self.book_return_amount_this_month()
        elif choice == 5:
            self.people_with_3_or_more_rentals()
        elif choice == 6:
            self.people_with_no_rentals_and_most()
        elif choice == 7:
            self.books_per_month()

    def authors_over_25(self):
        """
        Prints authors with age over 25
        """

        # Get the date for today, 25 years ago
        birth_date_25 = datetime.datetime.now()
        birth_date_25 = birth_date_25.replace(birth_date_25.year-25)

        # Filter to get authors with a birth_date before 'birth_date_25'
        authors = Author.objects.filter(birth_date__lte=birth_date_25)
        print("Authors that are +25 years old: ")
        for author in authors:
            print(author.name)

    def book_has_been_borrowed(self, book_id):
        """
        Prints how many times a BookUnit has been borrowed
        """
        book_rentals_amount = Rental.objects.filter(book_unit_id=book_id).count()
        book = BookUnit.objects.get(pk=book_id)
        print("The Book Unit "+book.__str__()+" has been borrowed "+str(book_rentals_amount)+" time(s)")

    def book_rental_amount_this_month(self):
        """
        Prints how many books have been borrowed this month
        """
        date = datetime.datetime.now()
        date = date.replace(day=1)
        date2 = next_month(date)

        rentals_last_month = Rental.objects.filter(rental_date__gte=make_aware(date), rental_date__lt=make_aware(date2))

        book_unit_rentals = rentals_last_month.values('book_unit_id')\
            .distinct()\
            .count()

        print(str(book_unit_rentals)+" books have been borrowed this month")

    def book_return_amount_this_month(self):
        """
        Prints how many books have been returned this month
        """
        date = datetime.datetime.now()
        date = date.replace(day=1)
        date2 = next_month(date)

        returns_last_month = Rental.objects.filter(return_date__gte=make_aware(date), return_date__lt=make_aware(date2))

        book_unit_returns = returns_last_month.values('book_unit_id')\
            .distinct()\
            .count()

        print(str(book_unit_returns)+" books have been returned this month")

    def people_with_3_or_more_rentals(self):
        """
        Prints the people that have more than 3 rentals
        """
        people = Person.objects.annotate(total=Count('rental')).filter(total__gte=3)

        if people:
            print("People that have made more than 3 rentals: ")
            for person in people:
                print(person)
        else:
            print("No one has more than 3 rentals")

    def people_with_no_rentals_and_most(self):
        """
        Prints the people with no rentals and the person with most rentals
        """
        people_with_no_rentals = Person.objects.filter(rental=None)

        person_with_most_rentals = Person.objects.annotate(Count('rental')).order_by('-rental__count').first()

        print("People with no rentals: \n")
        for person in people_with_no_rentals:
            print(person)

        print("\nThe person with most rentals is "+person_with_most_rentals.__str__()+" with "
              +str(person_with_most_rentals.rental__count)+" rentals")

    def books_per_month(self):
        date1 = datetime.datetime(2020, 1, 1)
        date2 = next_month(date1)
        end_date = datetime.datetime.now()

        while date1 < end_date:
            books_in_month = Rental.objects.filter(
                rental_date__gte=make_aware(date1), rental_date__lt=make_aware(date2)).count()
            print(str(date1)+": "+str(books_in_month)+" rentals")
            """
            Group by date
            """
            date1 = date1.replace(month=date1.month+1)
            date2 = next_month(date1)
