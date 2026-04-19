# 📚 Book Metadata and Recommendation API

**Course:** Web Services and Web Data (XJCO3011)  
**Date:** April 2026  
**Version:** 1.0.0

A comprehensive Django REST API for managing book metadata, user reviews, and intelligent recommendations.

## 🚀 Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Load sample data: `python manage.py load_sample_data`
4. Start server: `python manage.py runserver`
5. Visit API documentation: http://127.0.0.1:8000/swagger/

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd bookapi

# Install dependencies
pip install django djangorestframework django-filter drf-yasg

# Run migrations
python manage.py migrate

# Load sample data
python manage.py load_sample_data

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Access Points

- **API Root:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## ✨ Features

### Core Functionality
- ✅ **Complete CRUD Operations** - Create, Read, Update, Delete for all resources
- 📖 **Book Management** - Comprehensive book metadata
- 👤 **Author Management** - Author profiles and bibliographies
- 🏷️ **Genre Classification** - Organize books by categories
- ⭐ **Review System** - User ratings and comments
- 📋 **Reading Lists** - Personal book collections

### Advanced Features
- 🔍 **Full-Text Search** - Search across books, authors, and genres
- 🤖 **Smart Recommendations** - Content-based recommendation algorithm
- 📊 **Statistics & Analytics** - Real-time insights and popular books
- 🔐 **Authentication** - Secure user authentication
- 📄 **Auto-Generated Documentation** - Swagger/OpenAPI specs
- 🎨 **Interactive Documentation** - Swagger UI and ReDoc interfaces

## 📋 API Endpoints

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create new book
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book

### Authors
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Create new author
- `GET /api/authors/{id}/` - Get author details
- `PUT /api/authors/{id}/` - Update author
- `DELETE /api/authors/{id}/` - Delete author

### Genres
- `GET /api/genres/` - List all genres
- `POST /api/genres/` - Create new genre
- `GET /api/genres/{id}/` - Get genre details
- `PUT /api/genres/{id}/` - Update genre
- `DELETE /api/genres/{id}/` - Delete genre

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create review (auth required)
- `GET /api/reviews/{id}/` - Get review details
- `PUT /api/reviews/{id}/` - Update review (auth required)
- `DELETE /api/reviews/{id}/` - Delete review (auth required)

### Special Endpoints
- `GET /api/search/?q={query}` - Search books
- `GET /api/books/{id}/recommendations/` - Get recommendations
- `GET /api/popular/` - Get popular books
- `GET /api/statistics/` - Get system statistics
- `GET /api/reading-list/` - Get user's reading list (auth required)

## 🛠️ Technology Stack

- **Backend Framework:** Django 6.0.3
- **API Framework:** Django REST Framework 3.17.1
- **Database:** SQLite
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Filtering:** django-filter
- **Language:** Python 3.x

## 📊 Data Models

### Author
- Name, Biography, Birth Date, Nationality
- Automatic book count calculation

### Genre
- Name, Description
- Automatic book count calculation

### Book
- Title, Description, ISBN, Publisher
- Publication Date, Page Count, Language
- Many-to-Many: Authors, Genres
- Automatic rating calculations

### Review
- Book, User, Rating (1-5), Comment
- Unique constraint: One review per user per book

### ReadingList
- User, Book, Status (want_to_read, reading, completed)
- Unique constraint: One entry per user per book

## 🧪 Testing

### Using Swagger UI
1. Navigate to http://127.0.0.1:8000/swagger/
2. Select an endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

### Using ReDoc
1. Navigate to http://127.0.0.1:8000/redoc/
2. Browse the clean, organized documentation
3. View request/response examples
4. Copy code samples for your applications

### Sample Data
The project includes a management command to load sample data:

```bash
python manage.py load_sample_data
```

This creates:
- 7 Authors (J.K. Rowling, George Orwell, etc.)
- 7 Genres (Fantasy, Science Fiction, Mystery, etc.)
- 7 Books (Harry Potter, 1984, Pride and Prejudice, etc.)
- 12 Reviews
- 5 Test Users

## 📖 Documentation

- **Full API Documentation:** See `API_DOCUMENTATION.md`
- **Interactive Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc Documentation:** http://127.0.0.1:8000/redoc/

## 🔐 Authentication

### For Testing
Default test users (password: `testpass123`):
- testuser1
- testuser2
- testuser3
- testuser4
- testuser5

### For Admin
Create a superuser:
```bash
python manage.py createsuperuser
```

## 📁 Project Structure

```
bookapi/
├── bookapi/              # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
├── books/                # Main app
│   ├── models.py         # Data models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── admin.py          # Admin configuration
│   ├── urls.py           # App URL routes
│   └── management/       # Custom commands
│       └── commands/
│           └── load_sample_data.py
├── templates/            # HTML templates
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
├── README.md             # This file
└── API_DOCUMENTATION.md  # Full API docs
```

## 🎯 Key Features Demonstration

### 1. CRUD Operations
All models support full Create, Read, Update, Delete operations through RESTful endpoints.

### 2. Search Functionality
```bash
GET /api/search/?q=harry
```
Searches across book titles, descriptions, authors, genres, and publishers.

### 3. Recommendation Algorithm
```bash
GET /api/books/1/recommendations/
```
Content-based filtering using shared genres and authors to suggest similar books.

### 4. Statistics
```bash
GET /api/statistics/
```
Returns comprehensive system statistics including:
- Total counts (books, authors, genres, reviews)
- Average ratings
- Books by genre
- Top-rated books
- Most reviewed books

### 5. Filtering & Ordering
```bash
GET /api/books/?genres=1&ordering=-average_rating
```
Filter by genre and order by rating (descending).

## 🚧 Future Enhancements

- [ ] User authentication with JWT tokens
- [ ] Advanced recommendation algorithms (collaborative filtering)
- [ ] Book cover image upload
- [ ] Export functionality (CSV, PDF)
- [ ] Rate limiting
- [ ] Caching for improved performance
- [ ] Full-text search with Elasticsearch
- [ ] GraphQL API endpoint

## 📝 Assignment Information

**Course:** Web Services and Web Data (XJCO3011)  
**Type:** Individual Web Services API Development Project  
**Weight:** 30% of module grade  
**Submission:** GitHub + Minerva  

### Requirements Met
- ✅ CRUD operations for all resources
- ✅ 10+ API endpoints (exceeds requirement of 4)
- ✅ Database integration (SQLite)
- ✅ JSON responses with proper HTTP status codes
- ✅ RESTful API design
- ✅ Interactive documentation (Swagger UI)
- ✅ Search and filtering capabilities
- ✅ Advanced features (recommendations, statistics)
- ✅ Authentication for protected endpoints
- ✅ Comprehensive error handling


