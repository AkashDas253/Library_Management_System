from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import BookActivity, UserProfile
from rest_framework.authtoken.models import Token

class ActivityAPITestCase(APITestCase):



    def setUp(self):
        from library.models import Author, Book, UserProfile
        self.user = User.objects.create_user(username='member', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user, role='member')
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Author1', bio='Test bio')
        self.book = Book.objects.create(title='Book1', author=self.author, isbn_number='111', published_date='2025-01-01')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



    def test_log_activity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/activities/log/'
        data = {'activity_type': 'borrow', 'book': self.book.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookActivity.objects.count(), 1)



    def test_my_activity(self):
        BookActivity.objects.create(user=self.user_profile, activity_type='borrow', book=self.book)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = '/api/activities/my-activity/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)



    def test_non_member_cannot_log_activity(self):
        # Create a librarian user
        librarian = User.objects.create_user(username='librarian', password='testpass123')
        UserProfile.objects.create(user=librarian, role='librarian')
        librarian_token = Token.objects.create(user=librarian)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + librarian_token.key)
        url = '/api/activities/log/'
        data = {'activity_type': 'borrow', 'book': self.book.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_non_member_cannot_view_activity(self):
        # Create an admin user
        admin = User.objects.create_user(username='admin', password='testpass123')
        UserProfile.objects.create(user=admin, role='admin')
        admin_token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)
        url = '/api/activities/my-activity/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
