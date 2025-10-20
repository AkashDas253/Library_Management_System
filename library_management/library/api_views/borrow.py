# Borrow/Return Book API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from library.models import BorrowedBook, Book, UserProfile, MembershipType, Location
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
        from library.utils import get_auto_accept_virtual
        book_id = request.data.get('book')
        location_id = request.data.get('location')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        user_profile = UserProfile.objects.get(user=request.user)
        # Membership check
        if not user_profile.membership_type:
            return Response({'error': 'No membership plan assigned.'}, status=status.HTTP_403_FORBIDDEN)
        # Borrow limit check (pending or accepted, not returned)
        active_borrows = BorrowedBook.objects.filter(user_profile=user_profile, status__in=['pending','accepted'], return_date__isnull=True).count()
        max_books = user_profile.membership_type.max_books
        if active_borrows >= max_books:
            return Response({'error': f'Borrow limit reached ({max_books}).'}, status=status.HTTP_403_FORBIDDEN)
        # Check if book is already borrowed (pending/accepted, not returned)
        if BorrowedBook.objects.filter(book=book, status__in=['pending','accepted'], return_date__isnull=True).exists():
            return Response({'error': 'Book not available'}, status=status.HTTP_400_BAD_REQUEST)
        # Auto-accept virtual book borrow if config enabled and user is within limit
        data = request.data.copy()
        auto_accept = False
        if (
            book.book_type == 'virtual'
            and location.location_type == 'virtual'
            and get_auto_accept_virtual()
        ):
            auto_accept = True
        data['status'] = 'accepted' if auto_accept else 'pending'
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user_profile=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_request(self, request, pk=None):
        # Only librarian at the book's location can approve
        try:
            borrow = BorrowedBook.objects.get(pk=pk)
            librarian_profile = UserProfile.objects.get(user=request.user)
        except (BorrowedBook.DoesNotExist, UserProfile.DoesNotExist):
            return Response({'error': 'Request or user not found.'}, status=status.HTTP_404_NOT_FOUND)
        if librarian_profile.role != 'librarian':
            return Response({'error': 'Only librarians can approve.'}, status=status.HTTP_403_FORBIDDEN)
        # Compare librarian's library_branch (string) with borrow.location.name
        if not borrow.location or librarian_profile.library_branch != borrow.location.name:
            return Response({'error': 'Librarian not assigned to this location.'}, status=status.HTTP_403_FORBIDDEN)
        if borrow.status != 'pending':
            return Response({'error': 'Request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        borrow.status = 'accepted'
        borrow.transacted_by = librarian_profile
        borrow.save()
        return Response({'status': 'Request approved.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_request(self, request, pk=None):
        try:
            borrow = BorrowedBook.objects.get(pk=pk)
            librarian_profile = UserProfile.objects.get(user=request.user)
        except (BorrowedBook.DoesNotExist, UserProfile.DoesNotExist):
            return Response({'error': 'Request or user not found.'}, status=status.HTTP_404_NOT_FOUND)
        if librarian_profile.role != 'librarian':
            return Response({'error': 'Only librarians can reject.'}, status=status.HTTP_403_FORBIDDEN)
        if not borrow.location or librarian_profile.library_branch != borrow.location.name:
            return Response({'error': 'Librarian not assigned to this location.'}, status=status.HTTP_403_FORBIDDEN)
        if borrow.status != 'pending':
            return Response({'error': 'Request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)
        borrow.status = 'rejected'
        borrow.transacted_by = librarian_profile
        borrow.save()
        return Response({'status': 'Request rejected.'}, status=status.HTTP_200_OK)

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
