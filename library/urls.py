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
]