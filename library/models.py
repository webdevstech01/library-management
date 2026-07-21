from django.db import models
from datetime import date
from django.db.models import PROTECT

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)

    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

PENALTY_PER_DAY = 1

class Loan(models.Model):
    member = models.ForeignKey(
    Member,
    on_delete=models.PROTECT,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
    )
    borrowed_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    @property
    def is_returned(self):
        return self.returned_at is not None

    @property
    def is_overdue(self):
        return (
            self.returned_at is None
            and self.due_date < date.today()
        )

    @property
    def status(self):
        if self.is_returned:
            return "Returned"

        if self.is_overdue:
            return "Overdue"

        return "Active"

    @property
    def penalty(self):
        end_date = self.returned_at or date.today()

        overdue_days = (end_date - self.due_date).days

        if overdue_days <= 0:
            return 0

        return overdue_days * PENALTY_PER_DAY

    def __str__(self):
        return f"{self.member} borrowed {self.book}"