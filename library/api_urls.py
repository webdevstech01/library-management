from django.urls import path

from .views import (
    BookListCreateView,
    BookDetailView,
    MemberListCreateView,
    MemberDetailView,
    BorrowBookView,
    ReturnBookView,
    ActiveLoansView,
    OverdueLoansView,
)

urlpatterns = [
    path("books/", BookListCreateView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),

    path("members/", MemberListCreateView.as_view()),
    path("members/<int:pk>/", MemberDetailView.as_view()),

    path("borrow/", BorrowBookView.as_view()),
    path("return/", ReturnBookView.as_view()),

    path("loans/active/", ActiveLoansView.as_view()),
    path("loans/overdue/", OverdueLoansView.as_view()),
]