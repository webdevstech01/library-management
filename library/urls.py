from django.urls import path
from . import views

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books, name="books"),
    path("members/", views.members, name="members"),
    path("loans/", views.loans, name="loans"),

    path(
        "login/",
        LoginView.as_view(
            template_name="library/login.html",
        ),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "books/add/",
        views.add_book,
        name="add_book",
    ),
    path(
        "books/<int:book_id>/edit/",
        views.edit_book,
        name="edit_book",
    ),

    path(
        "books/<int:book_id>/delete/",
        views.delete_book,
        name="delete_book",
    ),
        path(
        "members/add/",
        views.add_member,
        name="add_member",
    ),

    path(
        "members/<int:member_id>/edit/",
        views.edit_member,
        name="edit_member",
    ),

    path(
        "members/<int:member_id>/delete/",
        views.delete_member,
        name="delete_member",
    ),
    path(
        "loans/<int:loan_id>/return/",
        views.return_book_html,
        name="return_book_html",
    ),
    path(
        "books/<int:book_id>/borrow/",
        views.borrow_book_view,
        name="borrow_book",
    )
]