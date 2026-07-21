# 📚 Library Management System

A Library Management System built with **Django** and **Django REST Framework**.

The application allows librarians to manage books, members and loans while enforcing common library business rules such as book availability and borrowing limits.

---

## ✨ Features

### Books

- View all books
- Add a new book
- Edit existing books
- Delete books (protected if loan history exists)
- Search books by:
  - Title
  - Author
  - ISBN
  - Category
- Filter books by:
  - Category
  - Availability

### Members

- Register new members
- Edit member information
- Delete members (protected if loan history exists)
- View all members

### Loans

- Borrow books
- Return books
- View active loans
- View overdue loans
- Automatic due date (14 days)
- Automatic penalties added

### Authentication

- Login / Logout
- Staff-only access for administrative actions

### REST API

- Books
- Members
- Borrow book
- Return book
- Active loans
- Overdue loans

---

## 📌 Business Rules

The application enforces several business rules:

- A book cannot be borrowed if there are no available copies.
- A member cannot have more than **3 active loans**.
- A member cannot borrow the same book twice simultaneously.
- Books and members with loan history cannot be deleted.

---

## 🛠 Technologies

- Python 3.14
- Django 6
- Django REST Framework
- SQLite
- Bootstrap 5

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/library-management.git
```

Move into the project

```bash
cd library-management
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create an admin user

```bash
python manage.py createsuperuser
```

Start the server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000
```

---

## 📂 Project Structure

```
library/
│
├── models.py
├── views.py
├── forms.py
├── serializers.py
├── services.py
├── tests.py
├── urls.py
├── api_urls.py
│
├── templates/
│
└── migrations/
```

---

## 🧪 Tests

Run the test suite with:

```bash
python manage.py test
```

---

## 🔮 Future Improvements

- Member accounts
- Reservations
- Late return penalties
- Email notifications
- Pagination
