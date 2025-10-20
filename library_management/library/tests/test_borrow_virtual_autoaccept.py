from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import Book, BorrowedBook, UserProfile, MembershipType, Location, Author
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
import os

class BorrowVirtualAutoAcceptTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Write config.ini to the exact path used by the app code before any test runs
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config.ini'))
        with open(config_path, 'w') as f:
            f.write('[Borrow]\nauto_accept_virtual = true\n')

    def setUp(self):
        self.virtual_location = Location.objects.create(name='Virtual Library', location_type='virtual')
        self.physical_location = Location.objects.create(name='Physical Library', location_type='physical')
        self.membership = MembershipType.objects.create(name='Gold', monthly_price=10.0, max_books=2)
        self.member = User.objects.create_user(username='member', password='testpass123')
        self.member_profile = UserProfile.objects.create(user=self.member, role='member', membership_type=self.membership)
        self.token = Token.objects.create(user=self.member)
        self.author = Author.objects.create(name='Author1', bio='Test bio')
        self.virtual_book = Book.objects.create(title='VirtualBook', author=self.author, isbn_number='222', published_date='2025-01-01', book_type='virtual', location=self.virtual_location)
        self.physical_book = Book.objects.create(title='PhysicalBook', author=self.author, isbn_number='333', published_date='2025-01-01', book_type='physical', location=self.physical_location)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_virtual_book_virtual_location_auto_accept(self):
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.virtual_book.id, 'location': self.virtual_location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrow = BorrowedBook.objects.get(book=self.virtual_book, user_profile=self.member_profile)
        self.assertEqual(borrow.status, 'accepted')

    def test_virtual_book_physical_location_pending(self):
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.virtual_book.id, 'location': self.physical_location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrow = BorrowedBook.objects.get(book=self.virtual_book, user_profile=self.member_profile, location=self.physical_location)
        self.assertEqual(borrow.status, 'pending')

    def test_physical_book_virtual_location_pending(self):
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.physical_book.id, 'location': self.virtual_location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrow = BorrowedBook.objects.get(book=self.physical_book, user_profile=self.member_profile, location=self.virtual_location)
        self.assertEqual(borrow.status, 'pending')

    def test_virtual_book_virtual_location_auto_accept_limit(self):
        # Fill up borrow limit
        for _ in range(self.membership.max_books):
            BorrowedBook.objects.create(book=self.virtual_book, user_profile=self.member_profile, location=self.virtual_location, due_date=date.today() + timedelta(days=7), status='accepted')
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.virtual_book.id, 'location': self.virtual_location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
