from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Loan
from ..services import return_book

@staff_member_required
def loans(request):
    loans = Loan.objects.select_related(
    "book",
    "member",
    )

    return render(
        request,
        "library/loan_list.html",
        {
            "loans": loans,
        },
    )


@staff_member_required
def return_book_html(request, loan_id):

    loan = get_object_or_404(
        Loan,
        id=loan_id,
    )

    if request.method == "POST":

        return_book(loan)

    return redirect("loans")