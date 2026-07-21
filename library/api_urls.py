from django.urls import path

from . import api

urlpatterns = [
    path("books/", api.BookListCreateView.as_view()),
    path("books/<int:pk>/", api.BookDetailView.as_view()),

    path("members/", api.MemberListCreateView.as_view()),
    path("members/<int:pk>/", api.MemberDetailView.as_view()),

    path("borrow/", api.BorrowBookView.as_view()),
    path("return/", api.ReturnBookView.as_view()),

    path("loans/active/", api.ActiveLoansView.as_view()),
    path("loans/overdue/", api.OverdueLoansView.as_view()),
]