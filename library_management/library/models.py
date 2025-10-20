
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name


BOOK_TYPE_CHOICES = [
    ('physical', 'Physical'),
    ('virtual', 'Virtual'),
]
BOOK_STATUS_CHOICES = [
    ('available', 'Available'),
    ('racked', 'Racked'),
    ('discarded', 'Discarded'),
    ('purchased', 'Purchased'),
]

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES, default='physical')
    available_copies = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=BOOK_STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title


class MembershipType(models.Model):
    name = models.CharField(max_length=50)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_books = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
        ('self_checkout', 'Self Checkout'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # for librarian
    library_branch = models.CharField(max_length=100, blank=True, null=True)  # for librarian
    region = models.CharField(max_length=100, blank=True, null=True)  # for member
    membership_type = models.ForeignKey(MembershipType, on_delete=models.SET_NULL, null=True, blank=True)  # for member

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, related_name='borrowed_books', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, related_name='borrowed_books', on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    transacted_by = models.ForeignKey(UserProfile, related_name='transactions', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user_profile.user.username}"

class BookActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('borrow', 'Borrow'),
        ('return', 'Return'),
        ('rack', 'Rack'),
        ('purchase', 'Purchase'),
        ('discard', 'Discard'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
