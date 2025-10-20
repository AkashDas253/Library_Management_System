from django.contrib import admin
from .models import Author, Book, BorrowedBook, UserProfile, MembershipType, Location

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowedBook)
admin.site.register(UserProfile)
admin.site.register(MembershipType)
admin.site.register(Location)
