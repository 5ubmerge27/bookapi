from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Author, Genre, Book, Review
from datetime import date
import random


class Command(BaseCommand):
    help = 'Load sample data for testing the Book API'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create sample authors
        authors_data = [
            {'name': 'J.K. Rowling', 'nationality': 'British', 'birth_date': date(1965, 7, 31)},
            {'name': 'George Orwell', 'nationality': 'British', 'birth_date': date(1903, 6, 25)},
            {'name': 'Jane Austen', 'nationality': 'British', 'birth_date': date(1775, 12, 16)},
            {'name': 'Agatha Christie', 'nationality': 'British', 'birth_date': date(1890, 9, 15)},
            {'name': 'Stephen King', 'nationality': 'American', 'birth_date': date(1947, 9, 21)},
            {'name': 'Harper Lee', 'nationality': 'American', 'birth_date': date(1926, 4, 28)},
            {'name': 'F. Scott Fitzgerald', 'nationality': 'American', 'birth_date': date(1896, 9, 24)},
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults=author_data
            )
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.name}')
        
        # Create sample genres
        genres_data = [
            {'name': 'Fantasy', 'description': 'Fantasy literature'},
            {'name': 'Science Fiction', 'description': 'Science fiction literature'},
            {'name': 'Mystery', 'description': 'Mystery and detective fiction'},
            {'name': 'Romance', 'description': 'Romance literature'},
            {'name': 'Horror', 'description': 'Horror fiction'},
            {'name': 'Classic', 'description': 'Classic literature'},
            {'name': 'Young Adult', 'description': 'Young adult fiction'},
        ]
        
        genres = []
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults=genre_data
            )
            genres.append(genre)
            if created:
                self.stdout.write(f'Created genre: {genre.name}')
        
        # Create sample books
        books_data = [
            {
                'title': "Harry Potter and the Philosopher's Stone",
                'description': 'The first book in the Harry Potter series.',
                'isbn': '9780747532699',
                'publication_date': date(1997, 6, 26),
                'publisher': 'Bloomsbury',
                'page_count': 223,
                'language': 'English',
                'authors': ['J.K. Rowling'],
                'genres': ['Fantasy', 'Young Adult']
            },
            {
                'title': '1984',
                'description': 'A dystopian social science fiction novel.',
                'isbn': '9780451524935',
                'publication_date': date(1949, 6, 8),
                'publisher': 'Secker & Warburg',
                'page_count': 328,
                'language': 'English',
                'authors': ['George Orwell'],
                'genres': ['Science Fiction', 'Classic']
            },
            {
                'title': 'Pride and Prejudice',
                'description': 'A romantic novel of manners.',
                'isbn': '9780141439518',
                'publication_date': date(1813, 1, 28),
                'publisher': 'T. Egerton',
                'page_count': 432,
                'language': 'English',
                'authors': ['Jane Austen'],
                'genres': ['Romance', 'Classic']
            },
            {
                'title': 'Murder on the Orient Express',
                'description': 'A detective novel featuring Hercule Poirot.',
                'isbn': '9780007119318',
                'publication_date': date(1934, 1, 1),
                'publisher': 'Collins Crime Club',
                'page_count': 256,
                'language': 'English',
                'authors': ['Agatha Christie'],
                'genres': ['Mystery', 'Classic']
            },
            {
                'title': 'The Shining',
                'description': 'A horror novel about a haunted hotel.',
                'isbn': '9780307743657',
                'publication_date': date(1977, 1, 28),
                'publisher': 'Doubleday',
                'page_count': 447,
                'language': 'English',
                'authors': ['Stephen King'],
                'genres': ['Horror']
            },
            {
                'title': 'To Kill a Mockingbird',
                'description': 'A novel about racial injustice and childhood.',
                'isbn': '9780061120084',
                'publication_date': date(1960, 7, 11),
                'publisher': 'J.B. Lippincott & Co.',
                'page_count': 376,
                'language': 'English',
                'authors': ['Harper Lee'],
                'genres': ['Classic']
            },
            {
                'title': 'The Great Gatsby',
                'description': 'A novel about the American Dream.',
                'isbn': '9780743273565',
                'publication_date': date(1925, 4, 10),
                'publisher': 'Charles Scribner\'s Sons',
                'page_count': 180,
                'language': 'English',
                'authors': ['F. Scott Fitzgerald'],
                'genres': ['Classic']
            },
        ]
        
        books = []
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={k: v for k, v in book_data.items() if k not in ['authors', 'genres']}
            )
            
            if created:
                # Add authors
                for author_name in book_data['authors']:
                    author = Author.objects.get(name=author_name)
                    book.authors.add(author)
                
                # Add genres
                for genre_name in book_data['genres']:
                    genre = Genre.objects.get(name=genre_name)
                    book.genres.add(genre)
                
                books.append(book)
                self.stdout.write(f'Created book: {book.title}')
        
        # Create sample users for reviews
        test_users = []
        for i in range(5):
            username = f'testuser{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Test{i+1}',
                    'last_name': 'User'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            test_users.append(user)
        
        # Create sample reviews
        for book in books:
            # Random number of reviews per book (1-3)
            num_reviews = random.randint(1, 3)
            selected_users = random.sample(test_users, num_reviews)
            
            for user in selected_users:
                rating = random.randint(3, 5)  # Good ratings for sample data
                comments = [
                    "Great book! Highly recommend.",
                    "Really enjoyed reading this.",
                    "A classic that everyone should read.",
                    "Excellent storytelling and character development.",
                    "One of my favorite books of all time.",
                ]
                
                review, created = Review.objects.get_or_create(
                    book=book,
                    user=user,
                    defaults={
                        'rating': rating,
                        'comment': random.choice(comments)
                    }
                )
                
                if created:
                    self.stdout.write(f'Created review for {book.title} by {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
        self.stdout.write(f'Created {Author.objects.count()} authors')
        self.stdout.write(f'Created {Genre.objects.count()} genres')
        self.stdout.write(f'Created {Book.objects.count()} books')
        self.stdout.write(f'Created {Review.objects.count()} reviews')
