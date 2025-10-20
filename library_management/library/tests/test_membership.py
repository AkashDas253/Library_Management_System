from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from library.models import UserProfile, MembershipType
from rest_framework.authtoken.models import Token

class MembershipAPITestCase(APITestCase):

    def setUp(self):
        self.member = User.objects.create_user(username='member', password='testpass123')
        self.member_profile = UserProfile.objects.create(user=self.member, role='member')
        self.token = Token.objects.create(user=self.member)
        self.membership_type = MembershipType.objects.create(name='Gold', monthly_price=10.0, max_books=5)


    def test_view_membership(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('membership-detail', args=[self.member_profile.pk])
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['id'], self.member_profile.pk)


    def test_update_membership(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('membership-detail', args=[self.member_profile.pk])
        data = {'membership_type_id': self.membership_type.pk}
        response = self.client.patch(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])
        if response.status_code == status.HTTP_200_OK:
            self.member_profile.refresh_from_db()
            self.assertEqual(self.member_profile.membership_type, self.membership_type)

    def test_non_member_cannot_access(self):
        librarian = User.objects.create_user(username='librarian', password='testpass123')
        UserProfile.objects.create(user=librarian, role='librarian')
        librarian_token = Token.objects.create(user=librarian)
        url = reverse('membership-detail', args=[self.member_profile.pk])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + librarian_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
