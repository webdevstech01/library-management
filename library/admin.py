from django.contrib import admin
from .models import Book
from .models import Member
from .models import Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "available_copies",
        "total_copies",
    )

    search_fields = (
        "title",
        "author",
        "isbn",
    )

    list_filter = (
        "category",
    )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
    )

    search_fields = (
        "member__last_name",
        "member__email",
        "book__title",
        "book__author",
    )

    list_filter = (
        "book",
        "borrowed_at",
        "due_date",
    )

 