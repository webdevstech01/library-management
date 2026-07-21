from datetime import date, timedelta

from django.db import transaction

from .models import Book, Loan, Member

@transaction.atomic
def borrow_book(member: Member, book: Book) -> Loan:
    if book.available_copies == 0:
        raise ValueError("There are no available copies left.")

    existing_loan = Loan.objects.filter(
    member=member,
    book=book,
    returned_at__isnull=True,
    ).exists()

    if existing_loan:
        raise ValueError(
            "This member already has this book borrowed."
        )

    active_loans = Loan.objects.filter(
        member=member,
        returned_at__isnull=True,
    ).count()

    if active_loans >= 3:
        raise ValueError("Member already has 3 active loans.")

    due_date = date.today() + timedelta(days=14)

    loan = Loan.objects.create(
        member=member,
        book=book,
        due_date=due_date,
    )

    book.available_copies -= 1
    book.save()

    return loan

@transaction.atomic
def return_book(loan: Loan) -> Loan:
    if loan.returned_at is not None:
        raise ValueError("Book has already been returned.")

    loan.returned_at = date.today()
    loan.save()

    book = loan.book
    book.available_copies += 1
    book.save()

    return loan
    
def get_active_loans():
    return Loan.objects.select_related(
        "book",
        "member",
    ).filter(
        returned_at__isnull=True
    )


def get_overdue_loans():
    return Loan.objects.select_related(
        "book",
        "member",
    ).filter(
        returned_at__isnull=True,
        due_date__lt=date.today()
    )