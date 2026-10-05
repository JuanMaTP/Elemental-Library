# Elemental Library

[![CI](https://github.com/JuanMaTP/Elemental-Library/actions/workflows/ci.yml/badge.svg)](https://github.com/JuanMaTP/Elemental-Library/actions/workflows/ci.yml)

A REST API for a small library, built with Django REST Framework. People register and borrow book units; staff manage books, units and authors; a Celery task returns rentals that have been open for too long.

**Stack:** Python 3.12, Django 5.2, Django REST Framework, Simple JWT, django-filter, drf-spectacular (OpenAPI), Celery with Redis, PostgreSQL, Docker, pytest, GitHub Actions.

## Run it with Docker

```bash
docker compose up --build
```

This starts the API, PostgreSQL, Redis and a Celery worker with beat. Then open:

- http://localhost:8000/ for the Swagger UI
- http://localhost:8000/redoc/ for ReDoc
- http://localhost:8000/admin/ for the Django admin

Create an admin user and some random data:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py populate
```

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt

export DJANGO_DEBUG=true          # uses SQLite and a local secret key
python manage.py migrate
python manage.py runserver
```

Run the tests and the linter:

```bash
pytest
ruff check .
```

Settings come from environment variables; see [.env.example](.env.example). Without `DATABASE_URL` the app uses SQLite.

## Authentication

`POST /login/` with a username and password returns a JWT access token (valid for 20 minutes) and a refresh token. Send the access token as `Authorization: Bearer <token>`, and get a new one from `POST /api/token/refresh/`.

## Endpoints

| Endpoint | Methods | Who |
|---|---|---|
| `/api/people/` | GET list, POST register | anyone |
| `/api/people/{id}/` | GET; PUT, PATCH, DELETE | anyone can read; only the user themselves can change it |
| `/api/books/` | GET list, POST | anyone can read; staff create |
| `/api/books/{id}/` | GET, PUT, PATCH, DELETE; POST adds a book unit | anyone can read; staff change |
| `/api/books/units/` | GET list of book units | anyone |
| `/api/books/{book_id}/{id}/` | GET, PUT, PATCH, DELETE one book unit | anyone can read; staff change |
| `/api/authors/`, `/api/authors/{id}/` | CRUD | anyone can read; staff change |
| `/api/rentals/` | GET list | logged-in users |
| `/api/rentals/borrow/` | POST `{"book_unit": id}` | logged-in people |
| `/api/rentals/return/{id}/` | PUT | the person who borrowed it, or staff |
| `/api/rentals/{id}/` | GET; PUT, PATCH, DELETE | logged-in users can read; staff change |

List endpoints support pagination (`?page=`, `?page_size=`), filters (for example `/api/books/?name=dune`, `/api/rentals/?book_name=dune&rental_date_gte=2026-01-01T00:00`) and ordering (`?ordering=name` or `?ordering=-name`).

## How it works

- A **Book** has any number of **Authors** and **BookUnits** (physical copies, each with a unique 16-character serial).
- A **Person** extends Django's user with a birth date, gender, type (student, teacher or visitor) and a picture.
- A **Rental** links a person to a book unit. Borrowing marks the unit as borrowed; returning sets the return date and makes it available again. A unit that is already borrowed can't be borrowed twice.
- Every hour, the Celery task `rental.tasks.check_rentals_return` returns rentals that have been open longer than `RENTAL_PERIOD_DAYS` (14 by default).
- `python manage.py queries --choice 1..7` runs a few example reports, such as rentals per month or people with the most rentals.

## History

I built this in 2020 as a Django REST practice project. In 2026 I brought it up to date:

- upgraded from Django 3.1 to Django 5.2 and to current versions of every library, replacing the unmaintained drf-yasg and django-rest-swagger with drf-spectacular
- moved the secret key, debug flag and database to environment variables, with PostgreSQL support
- fixed bugs: write permissions that allowed anyone to edit books and authors, borrowing that looked up the person by the user's id, any change to a rental freeing its book unit, and a hard-coded time-zone offset in the overdue task
- added the missing migrations, more tests (24 in total), Docker, docker-compose and GitHub Actions CI
