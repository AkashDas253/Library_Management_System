# Activity Tracking API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from library.models import BookActivity, UserProfile
from library.serializers import BookActivitySerializer


# Only allow users with the 'member' role
class IsMemberOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'member'
        except UserProfile.DoesNotExist:
            return False


class BookActivityViewSet(viewsets.ModelViewSet):
    queryset = BookActivity.objects.all()
    serializer_class = BookActivitySerializer
    permission_classes = [IsMemberOnly]

    def get_user_profile(self, user):
        return UserProfile.objects.get(user=user)

    @action(detail=False, methods=['get'], url_path='my-activity')
    def my_activity(self, request):
        user_profile = self.get_user_profile(request.user)
        activities = BookActivity.objects.filter(user=user_profile)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='log')
    def log_activity(self, request):
        user_profile = self.get_user_profile(request.user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
