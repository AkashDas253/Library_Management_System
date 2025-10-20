# Book Management API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from library.models import Book, UserProfile
from library.serializers import BookSerializer

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'librarian'
        except UserProfile.DoesNotExist:
            return False

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return [permissions.IsAuthenticated()]
