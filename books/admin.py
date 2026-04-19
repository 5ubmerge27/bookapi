from django.contrib import admin
from .models import Author, Genre, Book, Review, ReadingList


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_date', 'created_at')
    list_filter = ('nationality', 'birth_date')
    search_fields = ('name', 'biography')
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date', 'average_rating', 'ratings_count', 'created_at')
    list_filter = ('genres', 'language', 'publication_date', 'publisher')
    search_fields = ('title', 'description', 'isbn')
    filter_horizontal = ('authors', 'genres')
    ordering = ('-created_at',)
    readonly_fields = ('average_rating', 'ratings_count')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'comment')
    ordering = ('-created_at',)


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'added_at')
    list_filter = ('status', 'added_at')
    search_fields = ('user__username', 'book__title')
    ordering = ('-added_at',)
