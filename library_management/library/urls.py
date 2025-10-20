from django.urls import path, include
from .api_views.auth import RegisterView, LoginView
from .api_views.book import BookViewSet
from .api_views.borrow import BorrowedBookViewSet
from .api_views.activity import BookActivityViewSet
from .api_views.membership import MembershipViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/books', BookViewSet, basename='book')
router.register(r'api/borrowedbooks', BorrowedBookViewSet, basename='borrowedbook')
router.register(r'api/activities', BookActivityViewSet, basename='activity')
router.register(r'api/membership', MembershipViewSet, basename='membership')

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls
