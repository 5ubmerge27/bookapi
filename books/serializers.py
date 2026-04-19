from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Genre, Book, Review, ReadingList


class AuthorSerializer(serializers.ModelSerializer):
    """作者序列化器"""
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'nationality', 
                 'books_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_books_count(self, obj):
        return obj.books.count()


class GenreSerializer(serializers.ModelSerializer):
    """分类序列化器"""
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books_count', 'created_at']
        read_only_fields = ['created_at']
    
    def get_books_count(self, obj):
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    """图书列表序列化器（简化版）"""
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'average_rating', 
                 'ratings_count', 'cover_image_url', 'publication_date']


class BookDetailSerializer(serializers.ModelSerializer):
    """图书详情序列化器"""
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), 
        many=True, 
        write_only=True,
        source='authors'
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), 
        many=True, 
        write_only=True,
        source='genres'
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'author_ids', 'genre_ids',
                 'isbn', 'description', 'publication_date', 'publisher', 
                 'page_count', 'language', 'average_rating', 'ratings_count',
                 'cover_image_url', 'created_at', 'updated_at']
        read_only_fields = ['average_rating', 'ratings_count', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user = UserSerializer(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'book', 'book_title', 'user', 'rating', 'comment', 
                 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReadingListSerializer(serializers.ModelSerializer):
    """阅读清单序列化器"""
    user = UserSerializer(read_only=True)
    book = BookListSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'
    )
    
    class Meta:
        model = ReadingList
        fields = ['id', 'user', 'book', 'book_id', 'status', 'added_at', 'updated_at']
        read_only_fields = ['user', 'added_at', 'updated_at']
    
    def create(self, validated_data):
        # 自动设置当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookRecommendationSerializer(serializers.Serializer):
    """图书推荐序列化器"""
    book = BookListSerializer()
    similarity_score = serializers.FloatField()
    reason = serializers.CharField()
