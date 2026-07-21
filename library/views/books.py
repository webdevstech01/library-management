from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import BookForm, BorrowBookForm, BookFilterForm
from ..models import Book
from ..services import borrow_book
from django.urls import reverse

def books(request):

    form = BookFilterForm(request.GET)

    books = Book.objects.all()

    if form.is_valid():

        search = form.cleaned_data["search"]
        category = form.cleaned_data["category"]
        availability = form.cleaned_data["availability"]

        if search:

            books = books.filter(
                Q(title__icontains=search)
                | Q(author__icontains=search)
                | Q(isbn__icontains=search)
                | Q(category__icontains=search)
            )

        if category:

            books = books.filter(
                category=category,
            )

        if availability == "available":

            books = books.filter(
                available_copies__gt=0,
            )

        elif availability == "unavailable":

            books = books.filter(
                available_copies=0,
            )

    return render(
        request,
        "library/book_list.html",
        {
            "books": books,
            "filter_form": form,
        },
    )

@staff_member_required
def add_book(request):

    if request.method == "POST":

        form = BookForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("books")

    else:

        form = BookForm()

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Adauga carte",
            "cancel_url": reverse("books"),
        },
    )

@staff_member_required
def edit_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id,
    )

    if request.method == "POST":

        form = BookForm(
            request.POST,
            instance=book,
        )

        if form.is_valid():

            form.save()

            return redirect("books")

    else:

        form = BookForm(
            instance=book,
        )

    return render(
        request,
        "library/form.html",
        {
            "form": form,
            "title": "Editeaza carte",
            "cancel_url": reverse("books"),
        },
    )


@staff_member_required
def delete_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id,
    )

    if request.method == "POST":

        try:

            book.delete()

            messages.success(
                request,
                "Book deleted successfully.",
            )

        except ProtectedError:

            messages.error(
                request,
                "Cannot delete this book because it has loan history.",
            )

        return redirect("books")

    return render(
        request,
        "library/book_confirm_delete.html",
        {
            "book": book,
        },
    )

@staff_member_required
def borrow_book_view(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id,
    )

    if request.method == "POST":

        form = BorrowBookForm(request.POST)

        if form.is_valid():

            try:

                borrow_book(
                    form.cleaned_data["member"],
                    book,
                )

                messages.success(
                    request,
                    "Book borrowed successfully.",
                )

                return redirect("loans")

            except ValueError as e:

                form.add_error(
                    None,
                    str(e),
                )

    else:

        form = BorrowBookForm()

    return render(
        request,
        "library/borrow_book.html",
        {
            "book": book,
            "form": form,
        },
    )
