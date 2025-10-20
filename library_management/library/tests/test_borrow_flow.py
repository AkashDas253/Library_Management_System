from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import Book, BorrowedBook, UserProfile, MembershipType, Location
from rest_framework.authtoken.models import Token
from datetime import date, timedelta

class BorrowFlowTestCase(APITestCase):
    def setUp(self):
        self.location = Location.objects.create(name='Main Library', location_type='physical', address='123 Main St')
        self.virtual_location = Location.objects.create(name='Virtual Library', location_type='virtual')
        self.membership = MembershipType.objects.create(name='Gold', monthly_price=10.0, max_books=2)
        self.member = User.objects.create_user(username='member', password='testpass123')
        self.member_profile = UserProfile.objects.create(user=self.member, role='member', membership_type=self.membership)
        self.librarian = User.objects.create_user(username='librarian', password='testpass123')
        self.librarian_profile = UserProfile.objects.create(user=self.librarian, role='librarian', library_branch=self.location.name)
        self.token = Token.objects.create(user=self.member)
        self.librarian_token = Token.objects.create(user=self.librarian)
        from library.models import Author
        self.author = Author.objects.create(name='Author1', bio='Test bio')
        self.book = Book.objects.create(title='Book1', author=self.author, isbn_number='111', published_date='2025-01-01', available_copies=1, location=self.location)

    def test_borrow_request_pending(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.book.id, 'location': self.location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrow = BorrowedBook.objects.get(book=self.book, user_profile=self.member_profile)
        self.assertEqual(borrow.status, 'pending')

    def test_borrow_limit_enforced(self):
        # Create max allowed borrows
        for _ in range(self.membership.max_books):
            BorrowedBook.objects.create(book=self.book, user_profile=self.member_profile, location=self.location, due_date=date.today() + timedelta(days=7), status='accepted')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.book.id, 'location': self.location.id, 'due_date': str(date.today() + timedelta(days=7))}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_librarian_approve_request(self):
        borrow = BorrowedBook.objects.create(book=self.book, user_profile=self.member_profile, location=self.location, due_date=date.today() + timedelta(days=7), status='pending')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.librarian_token.key)
        url = f'/api/borrowedbooks/{borrow.id}/approve/'
        response = self.client.post(url)
        borrow.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(borrow.status, 'accepted')

    def test_librarian_reject_request(self):
        borrow = BorrowedBook.objects.create(book=self.book, user_profile=self.member_profile, location=self.location, due_date=date.today() + timedelta(days=7), status='pending')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.librarian_token.key)
        url = f'/api/borrowedbooks/{borrow.id}/reject/'
        response = self.client.post(url)
        borrow.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(borrow.status, 'rejected')

    def test_membership_change_blocked_with_active_borrows(self):
        # Create an active borrow
        BorrowedBook.objects.create(book=self.book, user_profile=self.member_profile, location=self.location, due_date=date.today() + timedelta(days=7), status='accepted')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = f'/api/membership/{self.member_profile.id}/'
        data = {'membership_type_id': self.membership.id}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
