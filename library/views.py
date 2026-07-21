from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from .models import Book, Member, Loan
from .serializers import BookSerializer, MemberSerializer, BorrowBookSerializer, ReturnBookSerializer, LoanSerializer

from .services import borrow_book, return_book, get_active_loans, get_overdue_loans

from django.contrib.auth.decorators import login_required

from .forms import BookForm,MemberForm,BorrowBookForm,BookFilterForm
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import ProtectedError

from django.db.models import Q
from datetime import date


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class BorrowBookView(APIView):

    def post(self, request):
        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = get_object_or_404(
            Member,
            id=serializer.validated_data["member_id"]
        )

        book = get_object_or_404(
            Book,
            id=serializer.validated_data["book_id"]
        )

        try:
            loan = borrow_book(member, book)

            return Response(
                {
                "message": "Book borrowed successfully.",
                "loan_id": loan.id,
                "member_id": member.id,
                "book_id": book.id,
                "due_date": loan.due_date,
            },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

class ReturnBookView(APIView):

    def post(self, request):

        serializer = ReturnBookSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        loan = get_object_or_404(
            Loan,
            id=serializer.validated_data["loan_id"]
        )

        try:
            return_book(loan)

            return Response(
                {
                    "message": "Book returned successfully.",
                    "loan_id": loan.id,
                    "member_id": loan.member.id,
                    "book_id": loan.book.id,
                    "returned_at": loan.returned_at,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

class ActiveLoansView(APIView):

    def get(self, request):
        loans = get_active_loans()

        serializer = LoanSerializer(
            loans,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

class OverdueLoansView(APIView):

    def get(self, request):
        loans = get_overdue_loans()

        serializer = LoanSerializer(
            loans,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

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
def members(request):
    members = Member.objects.all()

    return render(
        request,
        "library/member_list.html",
        {
            "members": members,
        },
    )

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
        "library/book_form.html",
        {
            "form": form,
            "title": "Add Book",
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
        "library/book_form.html",
        {
            "form": form,
            "title": "Edit Book",
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
def add_member(request):

    if request.method == "POST":

        form = MemberForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("members")

    else:

        form = MemberForm()

    return render(
        request,
        "library/member_form.html",
        {
            "form": form,
            "title": "Add Member",
        },
    )

@staff_member_required
def edit_member(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id,
    )

    if request.method == "POST":

        form = MemberForm(
            request.POST,
            instance=member,
        )

        if form.is_valid():

            form.save()

            return redirect("members")

    else:

        form = MemberForm(
            instance=member,
        )

    return render(
        request,
        "library/member_form.html",
        {
            "form": form,
            "title": "Edit Member",
        },
    )

@staff_member_required
def delete_member(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id,
    )

    if request.method == "POST":

        try:

            member.delete()

            messages.success(
                request,
                "Member deleted successfully.",
            )

        except ProtectedError:

            messages.error(
                request,
                "Cannot delete this member because they have loan history.",
            )

        return redirect("members")

    return render(
        request,
        "library/member_confirm_delete.html",
        {
            "member": member,
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

@staff_member_required
def return_book_html(request, loan_id):

    loan = get_object_or_404(
        Loan,
        id=loan_id,
    )

    if request.method == "POST":

        return_book(loan)

    return redirect("loans")