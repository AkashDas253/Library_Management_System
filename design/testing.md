# Testing Guide

This guide explains how to run and extend tests for the Library Management System.

---

## Running Tests

- To run all tests:
  ```powershell
  python manage.py test
  ```
- To run a specific test module (e.g., borrow tests):
  ```powershell
  python manage.py test library.tests.test_borrow --verbosity=2
  ```

---

## Test Structure

Tests are located in `library_management/library/tests/` and organized by feature:

- `test_auth.py` — Registration and login
- `test_book.py` — Book CRUD and permissions
- `test_borrow.py` — Borrowing and returning books
- `test_activity.py` — Activity logging and access
- `test_membership.py` — Membership view and update

Each test file uses Django's `APITestCase` for API-level testing.

---

## Best Practices

- Always run tests after making changes to models, views, or serializers.
- Add new tests for any new endpoint or feature.
- Use descriptive test method names (e.g., `test_member_can_borrow_book`).
- Use the DRF test client and set authentication tokens as needed.
- Check both success and failure cases (e.g., permissions, validation errors).

---

## Example: Adding a New Test

```python
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from library.models import Book, UserProfile
from rest_framework.authtoken.models import Token

class MyFeatureTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.profile = UserProfile.objects.create(user=self.user, role='member')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_my_feature(self):
        # Your test logic here
        response = self.client.get('/api/some-endpoint/')
        self.assertEqual(response.status_code, 200)
```

---

For more, see the existing test files and Django/DRF testing documentation.
