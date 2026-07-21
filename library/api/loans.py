from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.views import APIView

from ..models import Loan
from ..services import (
    return_book,
    get_active_loans,
    get_overdue_loans,
)
from ..services import borrow_book

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
