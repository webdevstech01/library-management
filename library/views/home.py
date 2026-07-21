from datetime import date

from django.shortcuts import render

from ..models import Book, Member, Loan

def home(request):

    books_count = Book.objects.count()

    members_count = Member.objects.count()

    active_loans = Loan.objects.filter(
        returned_at__isnull=True,
    ).count()

    overdue_loans = Loan.objects.filter(
        returned_at__isnull=True,
        due_date__lt=date.today(),
    ).count()

    return render(
        request,
        "library/home.html",
        {
            "books_count": books_count,
            "members_count": members_count,
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
        },
    )