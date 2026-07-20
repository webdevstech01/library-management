# Library Management System

A simple Library Management System built with Django and Django REST Framework.

## Features

- CRUD for books
- Member management
- Borrow and return books
- Active and overdue loans
- Business rules:
  - Maximum 3 active loans per member
  - Cannot borrow unavailable books
- Django Admin
- REST API (DRF)
- HTML interface
- Authentication (Login / Logout)
- Unit tests

## Technologies

- Python
- Django
- Django REST Framework
- SQLite
- Bootstrap 5

## Installation

```bash
git clone ...
cd library-management

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver