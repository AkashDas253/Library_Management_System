# Membership Management API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from library.models import UserProfile, MembershipType
from library.serializers import UserProfileMembershipSerializer

class IsMemberOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'member'
        except UserProfile.DoesNotExist:
            return False

class MembershipViewSet(viewsets.ViewSet):
    permission_classes = [IsMemberOnly]

    def retrieve(self, request, pk=None):
        # View own membership
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileMembershipSerializer(user_profile)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        # Update own membership (membership_type)
        user_profile = UserProfile.objects.get(user=request.user)
        # Check for active borrows
        active_borrows = user_profile.borrowed_books.filter(status__in=['pending','accepted'], return_date__isnull=True).count()
        if active_borrows > 0:
            return Response({'error': 'Cannot change membership type with active borrows.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserProfileMembershipSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
