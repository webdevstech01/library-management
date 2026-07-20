from django.test import TestCase

from .models import Book, Member
from .services import borrow_book, return_book


class LoanServiceTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name="Florinel",
            last_name="Test",
            email="test@test.com",
            phone="123456789",
        )

        self.book = Book.objects.create(
            title="Clean Code",
            author="Robert Martin",
            isbn="123456789",
            category="Programming",
            total_copies=5,
            available_copies=5,
        )

    def test_borrow_book_decreases_available_copies(self):
        borrow_book(self.member, self.book)

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            4
        )

    def test_return_book_increases_available_copies(self):
        loan = borrow_book(self.member, self.book)

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            4
        )

        return_book(loan)

        self.book.refresh_from_db()
        loan.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            5
        )

        self.assertIsNotNone(
            loan.returned_at
        )
    
    def test_member_cannot_have_more_than_three_active_loans(self):
        books = []

        for i in range(4):
            book = Book.objects.create(
                title=f"Book {i}",
                author="Author",
                isbn=f"12345678{i}",
                category="Programming",
                total_copies=1,
                available_copies=1,
            )

            books.append(book)

        borrow_book(self.member, books[0])
        borrow_book(self.member, books[1])
        borrow_book(self.member, books[2])

        with self.assertRaises(ValueError):
            borrow_book(self.member, books[3])