from rest_framework import viewsets
from .models import Book, Author, Member, BorrowedBook
from .serializers import BookSerializer, AuthorSerializer, MemberSerializer, BorrowedBookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
