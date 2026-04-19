from django.shortcuts import render
from django.db.models import Q, Count, Avg
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Author, Genre, Book, Review, ReadingList
from .serializers import (
    AuthorSerializer, GenreSerializer, BookListSerializer, 
    BookDetailSerializer, ReviewSerializer, ReadingListSerializer,
    BookRecommendationSerializer
)


# Author Views
class AuthorListCreateView(generics.ListCreateAPIView):
    """作者列表和创建视图"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'biography', 'nationality']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """作者详情视图"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Genre Views
class GenreListCreateView(generics.ListCreateAPIView):
    """分类列表和创建视图"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """分类详情视图"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


# Book Views
class BookListCreateView(generics.ListCreateAPIView):
    """图书列表和创建视图"""
    queryset = Book.objects.prefetch_related('authors', 'genres').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'authors__name', 'publisher']
    filterset_fields = ['genres', 'language', 'authors']
    ordering_fields = ['title', 'publication_date', 'average_rating', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookDetailSerializer
        return BookListSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """图书详情视图"""
    queryset = Book.objects.prefetch_related('authors', 'genres', 'reviews').all()
    serializer_class = BookDetailSerializer


# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
    """评论列表和创建视图"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Review.objects.select_related('user', 'book').all()


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """评论详情视图"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


# Reading List Views
class ReadingListView(generics.ListCreateAPIView):
    """阅读清单视图"""
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering = ['-added_at']
    
    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user).select_related('book')


class ReadingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    """阅读清单详情视图"""
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)


# Search and Recommendation Views
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'q',
            openapi.IN_QUERY,
            description="搜索关键词",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response('搜索结果', examples={
            'application/json': {
                'query': 'harry',
                'count': 1,
                'results': []
            }
        })
    }
)
@api_view(['GET'])
def search_books(request):
    """图书搜索API"""
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(authors__name__icontains=query) |
        Q(genres__name__icontains=query)
    ).distinct().prefetch_related('authors', 'genres')
    
    serializer = BookListSerializer(books, many=True)
    return Response({
        'query': query,
        'count': books.count(),
        'results': serializer.data
    })


@api_view(['GET'])
def book_recommendations(request, book_id):
    """基于内容的图书推荐API"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # 基于分类的推荐
    genre_recommendations = Book.objects.filter(
        genres__in=book.genres.all()
    ).exclude(id=book_id).distinct().prefetch_related('authors', 'genres')[:5]
    
    # 基于作者的推荐
    author_recommendations = Book.objects.filter(
        authors__in=book.authors.all()
    ).exclude(id=book_id).distinct().prefetch_related('authors', 'genres')[:3]
    
    # 使用字典来合并相同图书的推荐
    book_recommendations = {}
    
    # 添加分类推荐
    for rec_book in genre_recommendations:
        common_genres = set(book.genres.values_list('name', flat=True)) & \
                       set(rec_book.genres.values_list('name', flat=True))
        genre_score = len(common_genres) / max(len(book.genres.all()), 1)
        genre_reason = f"共同分类: {', '.join(common_genres)}"
        
        book_id = rec_book.id
        if book_id in book_recommendations:
            # 合并推荐：分数相加，理由合并
            book_recommendations[book_id]['similarity_score'] += genre_score
            book_recommendations[book_id]['reason'] += f" + {genre_reason}"
        else:
            book_recommendations[book_id] = {
                'book': BookListSerializer(rec_book).data,
                'similarity_score': genre_score,
                'reason': genre_reason
            }
    
    # 添加作者推荐
    for rec_book in author_recommendations:
        common_authors = set(book.authors.values_list('name', flat=True)) & \
                        set(rec_book.authors.values_list('name', flat=True))
        author_score = 0.8  # 同作者给高分
        author_reason = f"同作者: {', '.join(common_authors)}"
        
        book_id = rec_book.id
        if book_id in book_recommendations:
            # 合并推荐：分数相加，理由合并
            book_recommendations[book_id]['similarity_score'] += author_score
            book_recommendations[book_id]['reason'] += f" + {author_reason}"
        else:
            book_recommendations[book_id] = {
                'book': BookListSerializer(rec_book).data,
                'similarity_score': author_score,
                'reason': author_reason
            }
    
    # 转换为列表并按相似度排序
    recommendations = list(book_recommendations.values())
    recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return Response({
        'book': BookListSerializer(book).data,
        'recommendations': recommendations[:8]  # 返回前8个推荐
    })


@api_view(['GET'])
def popular_books(request):
    """热门图书API"""
    books = Book.objects.filter(
        average_rating__isnull=False,
        ratings_count__gte=1
    ).order_by('-average_rating', '-ratings_count').prefetch_related('authors', 'genres')[:20]
    
    serializer = BookListSerializer(books, many=True)
    return Response({
        'title': '热门图书',
        'books': serializer.data
    })


@api_view(['GET'])
def book_statistics(request):
    """图书统计API"""
    stats = {
        'total_books': Book.objects.count(),
        'total_authors': Author.objects.count(),
        'total_genres': Genre.objects.count(),
        'total_reviews': Review.objects.count(),
        'average_rating': Book.objects.aggregate(avg_rating=Avg('average_rating'))['avg_rating'],
        'books_by_genre': list(
            Genre.objects.annotate(book_count=Count('books')).values('name', 'book_count')
        ),
        'top_rated_books': BookListSerializer(
            Book.objects.filter(average_rating__isnull=False).order_by('-average_rating')[:5],
            many=True
        ).data
    }
    
    return Response(stats)
