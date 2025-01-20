from rest_framework import serializers
from .models import Book, Author, Member, BorrowedBook

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    member = MemberSerializer()

    class Meta:
        model = BorrowedBook
        fields = '__all__'
