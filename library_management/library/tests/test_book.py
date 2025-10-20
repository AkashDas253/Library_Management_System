from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import Book
from rest_framework.authtoken.models import Token

class BookAPITestCase(APITestCase):



    def setUp(self):
        from library.models import Author, UserProfile
        self.user = User.objects.create_user(username='librarian', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user, role='librarian')
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(name='Author Name', bio='Test bio')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'Test Book',
            'author': self.author.id,
            'isbn_number': '1234567890',
            'published_date': '2025-01-01'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)


    def test_list_books(self):
        Book.objects.create(title='Book1', author=self.author, isbn_number='111', published_date='2025-01-01')
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_update_book(self):
        book = Book.objects.create(title='Book2', author=self.author, isbn_number='222', published_date='2025-01-01')
        url = reverse('book-detail', args=[book.id])
        data = {'title': 'Updated Book'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, 'Updated Book')
