# library/tests/test_api.py

from rest_framework import status
from rest_framework.test import APITestCase
from library.models import Author, Book, Member, BorrowedBook
from django.utils import timezone
from datetime import timedelta


class LibraryAPITestCase(APITestCase):
    def setUp(self):
        # Set up initial data
        self.author = Author.objects.create(name="J.K. Rowling", bio="British author.")
        self.book = Book.objects.create(
            title="Harry Potter and the Sorcerer's Stone",
            author=self.author,
            published_date="1997-06-26",
            isbn_number="9780747532699",
            available_copies=5,
        )
        self.member = Member.objects.create(name="John Doe", email="john@example.com")
        self.borrowed_book = BorrowedBook.objects.create(
            book=self.book,
            member=self.member,
            borrowed_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=14),
        )

    def test_author_creation(self):
        url = "/api/authors/"
        data = {"name": "George R.R. Martin", "bio": "American novelist."}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "George R.R. Martin")

    # Add other test cases here...
