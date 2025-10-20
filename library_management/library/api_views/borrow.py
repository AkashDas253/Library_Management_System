# Borrow/Return Book API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from library.models import BorrowedBook, Book, UserProfile
from library.serializers import BorrowedBookSerializer

class IsMemberOrLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role in ['member', 'librarian']
        except UserProfile.DoesNotExist:
            return False

class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsMemberOrLibrarian]


    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow_book(self, request):
        book_id = request.data.get('book')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        # Check if book is already borrowed and not returned
        if BorrowedBook.objects.filter(book=book, return_date__isnull=True).exists():
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            serializer.save(user_profile=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        from django.utils import timezone
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            borrowed = BorrowedBook.objects.get(pk=pk, user_profile=user_profile, return_date__isnull=True)
        except (BorrowedBook.DoesNotExist, UserProfile.DoesNotExist):
            return Response({'error': 'Borrow record not found'}, status=status.HTTP_404_NOT_FOUND)
        borrowed.return_date = timezone.now().date()
        borrowed.save()
        return Response({'status': 'Book returned'}, status=status.HTTP_200_OK)
