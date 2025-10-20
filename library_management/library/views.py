from rest_framework import viewsets
from .models import Book, Author, BorrowedBook
from .serializers import BookSerializer, AuthorSerializer, BorrowedBookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
