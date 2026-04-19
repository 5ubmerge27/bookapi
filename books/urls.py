from django.urls import path
from . import views

urlpatterns = [
    # Author URLs
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Genre URLs
    path('genres/', views.GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    
    # Book URLs
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Review URLs
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Reading List URLs
    path('reading-list/', views.ReadingListView.as_view(), name='reading-list'),
    path('reading-list/<int:pk>/', views.ReadingListDetailView.as_view(), name='reading-list-detail'),
    
    # Search and Recommendation URLs
    path('search/', views.search_books, name='search-books'),
    path('books/<int:book_id>/recommendations/', views.book_recommendations, name='book-recommendations'),
    path('popular/', views.popular_books, name='popular-books'),
    path('statistics/', views.book_statistics, name='book-statistics'),
]
