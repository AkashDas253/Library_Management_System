from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, BorrowedBookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'borrowed', BorrowedBookViewSet, basename='borrowedbook')

urlpatterns = [
    path('', include(router.urls)),
]
