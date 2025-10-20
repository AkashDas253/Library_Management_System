from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthAPITestCase(APITestCase):
    def test_register(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        url = reverse('login')
        data = {
            'username': 'nouser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
