from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import Book, BorrowedBook, UserProfile
from rest_framework.authtoken.models import Token

class BorrowAPITestCase(APITestCase):


    def setUp(self):
        from library.models import Author, UserProfile, MembershipType, Location
        self.membership = MembershipType.objects.create(name='Gold', monthly_price=10.0, max_books=2)
        self.location = Location.objects.create(name='Main Library', location_type='physical', address='123 Main St')
        self.user = User.objects.create_user(username='member', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user, role='member', membership_type=self.membership)
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Author1', bio='Test bio')
        self.book = Book.objects.create(title='Book1', author=self.author, isbn_number='111', published_date='2025-01-01', available_copies=1, location=self.location)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



    def test_borrow_book(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.book.id, 'location': self.location.id, 'due_date': '2025-12-31'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BorrowedBook.objects.count(), 1)



    def test_borrow_unavailable_book(self):
        from datetime import date, timedelta
        BorrowedBook.objects.create(book=self.book, user_profile=self.user_profile, due_date='2025-12-31', location=self.location, status='accepted')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/borrowedbooks/borrow/'
        data = {'book': self.book.id, 'location': self.location.id, 'due_date': '2025-12-31'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_return_book(self):
        borrowed = BorrowedBook.objects.create(book=self.book, user_profile=self.user_profile, due_date='2025-12-31', location=self.location, status='accepted')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = f'/api/borrowedbooks/{borrowed.id}/return/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowed.refresh_from_db()
