from rest_framework.viewsets import ModelViewSet
from .models import Book, Member, BorrowedBook
from .serializers import BookSerializer, MemberSerializer, BorrowedBookSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class BorrowedBookViewSet(ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
