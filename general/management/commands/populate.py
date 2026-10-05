import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.crypto import get_random_string
from faker import Faker

from author.models import Author
from books.models import Book, BookUnit
from general.constants import Gender, Type
from person.models import Person
from rental.models import Rental


class Command(BaseCommand):
    help = 'Fill the database with random people, authors, books, book units and rentals'

    def handle(self, *args, **options):
        people_amount = random.randint(5, 10)
        authors_amount = random.randint(5, 10)
        books_amount = random.randint(5, 15)
        book_units_amount = random.randint(15, 50)
        rentals_amount = book_units_amount - random.randint(10, 14)

        self.populate_people(people_amount)
        self.populate_authors(authors_amount)
        self.populate_books(books_amount)
        self.populate_book_units(book_units_amount)
        self.populate_rentals(rentals_amount)

    def populate_rentals(self, amount):
        fake = Faker()
        for _ in range(amount):
            book_units = BookUnit.objects.all()
            while True:
                random_book_unit = random.choice(book_units)
                if not random_book_unit.borrowed:
                    break

            people = Person.objects.all()
            person = random.choice(list(people))
            person_type = person.type

            tz = timezone.get_current_timezone()
            rental_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=tz)
            percentage = random.randint(1, 100)
            return_date = None

            if percentage < 40:
                while True:
                    return_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=tz)

                    if return_date > rental_date:
                        break

                random_book_unit.borrowed = False
            else:
                random_book_unit.borrowed = True

            random_book_unit.save()
            if return_date:
                rental = Rental.objects.create(book_unit=random_book_unit, person=person, person_type=person_type,
                                               rental_date=rental_date, return_date=return_date)
                rental.rental_date = rental_date
                rental.save()
            else:
                rental = Rental.objects.create(book_unit=random_book_unit, person=person, person_type=person_type,
                                               rental_date=rental_date)

    def populate_book_units(self, amount):
        for _ in range(amount):
            books = Book.objects.all()
            random_book = random.choice(books)

            serial = get_random_string(length=16)

            BookUnit.objects.create(book=random_book, serial=serial)

    def populate_books(self, amount):
        fake = Faker()
        for _ in range(amount):
            name = fake.name()
            description = fake.text()

            authors = Author.objects.all()

            random_authors = random.sample(list(authors), random.randint(0, 3))

            book = Book.objects.create(name=name, description=description)

            book.author.add(*random_authors)

            book.save()

    def populate_authors(self, amount):
        for _ in range(amount):
            fake = Faker()
            name = fake.name()

            birth_date = fake.date_of_birth(minimum_age=15, maximum_age=60)

            gender_choices = [element for tuple in Gender.GENDER_CHOICES for element in tuple][::2]
            gender = random.choice(gender_choices)

            Author.objects.create(name=name, birth_date=birth_date, gender=gender)

    def populate_people(self, amount):
        fake = Faker()
        for _ in range(amount):
            username = fake.unique.user_name()
            password = make_password(get_random_string(random.randint(8, 15)))
            user = User.objects.create(username=username, password=password)

            birth_date = fake.date_of_birth(minimum_age=15, maximum_age=60)

            gender_choices = [element for tuple in Gender.GENDER_CHOICES for element in tuple][::2]
            gender = random.choice(gender_choices)

            type_choices = [element for tuple in Type.TYPE_CHOICES for element in tuple][::2]
            type = random.choice(type_choices)

            Person.objects.create(user=user, birth_date=birth_date, gender=gender, type=type)
