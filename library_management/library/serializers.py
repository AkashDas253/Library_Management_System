from rest_framework import serializers
from .models import Book, Author, BorrowedBook, BookActivity, MembershipType, UserProfile
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = '__all__'


class BorrowedBookSerializer(serializers.ModelSerializer):
    def validate(self, data):
        book = data.get('book')
        if book and book.available_copies is not None and book.available_copies < 1:
            raise serializers.ValidationError('No available copies for this book.')
        return data
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user_profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    transacted_by = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False, allow_null=True)

    class Meta:
        model = BorrowedBook
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class BookActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookActivity
        fields = '__all__'

class MembershipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipType
        fields = '__all__'

class UserProfileMembershipSerializer(serializers.ModelSerializer):
    membership_type = MembershipTypeSerializer(read_only=True)
    membership_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MembershipType.objects.all(), source='membership_type', write_only=True, required=False
    )
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'membership_type', 'membership_type_id', 'region']
        read_only_fields = ['id', 'user', 'role', 'membership_type', 'region']
