from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn_number = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, related_name='borrowed_books', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='borrowed_books', on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.name}"
