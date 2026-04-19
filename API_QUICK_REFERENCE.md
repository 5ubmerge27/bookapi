# 📋 Book API - Quick Reference Guide

## 🔗 Access URLs

| Service | URL |
|---------|-----|
| API Root | http://127.0.0.1:8000/ |
| Swagger UI | http://127.0.0.1:8000/swagger/ |
| ReDoc | http://127.0.0.1:8000/redoc/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

---

## 📚 Endpoints Summary

### Books
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/books/` | List all books | No |
| POST | `/api/books/` | Create book | No |
| GET | `/api/books/{id}/` | Get book details | No |
| PUT | `/api/books/{id}/` | Update book | No |
| DELETE | `/api/books/{id}/` | Delete book | No |

### Authors
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/authors/` | List all authors | No |
| POST | `/api/authors/` | Create author | No |
| GET | `/api/authors/{id}/` | Get author details | No |
| PUT | `/api/authors/{id}/` | Update author | No |
| DELETE | `/api/authors/{id}/` | Delete author | No |

### Genres
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/genres/` | List all genres | No |
| POST | `/api/genres/` | Create genre | No |
| GET | `/api/genres/{id}/` | Get genre details | No |
| PUT | `/api/genres/{id}/` | Update genre | No |
| DELETE | `/api/genres/{id}/` | Delete genre | No |

### Reviews
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/reviews/` | List all reviews | No |
| POST | `/api/reviews/` | Create review | **Yes** |
| GET | `/api/reviews/{id}/` | Get review details | No |
| PUT | `/api/reviews/{id}/` | Update review | **Yes** |
| DELETE | `/api/reviews/{id}/` | Delete review | **Yes** |

### Special Features
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/search/?q={query}` | Search books | No |
| GET | `/api/books/{id}/recommendations/` | Get recommendations | No |
| GET | `/api/popular/` | Popular books | No |
| GET | `/api/statistics/` | System statistics | No |
| GET | `/api/reading-list/` | User's reading list | **Yes** |
| POST | `/api/reading-list/` | Add to reading list | **Yes** |

---

## 🎯 Common Query Parameters

### Pagination
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10)

### Filtering (Books)
- `genres` - Filter by genre ID
- `authors` - Filter by author ID
- `language` - Filter by language

### Searching
- `search` - Search term (works on multiple fields)

### Ordering
- `ordering` - Order by field
  - Examples: `title`, `-created_at`, `average_rating`
  - Prefix with `-` for descending

---

## 📝 Request Examples

### Create a Book
```bash
POST /api/books/
Content-Type: application/json

{
  "title": "New Book",
  "description": "Book description",
  "isbn": "9781234567890",
  "publisher": "Publisher",
  "publication_date": "2026-01-01",
  "page_count": 300,
  "language": "English",
  "author_ids": [1],
  "genre_ids": [1, 2]
}
```

### Create a Review
```bash
POST /api/reviews/
Authorization: Basic <credentials>
Content-Type: application/json

{
  "book": 1,
  "rating": 5,
  "comment": "Great book!"
}
```

### Search Books
```bash
GET /api/search/?q=harry
```

### Filter and Order Books
```bash
GET /api/books/?genres=1&ordering=-average_rating
```

---

## 🔐 Authentication

### Test Users
Username: `testuser1` to `testuser5`  
Password: `testpass123`

### Authentication Methods
- Session Authentication (browser)
- Basic Authentication (API clients)

### Protected Endpoints
- Creating/updating/deleting reviews
- Managing reading lists

---

## 📊 Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 204 | No Content - Deleted successfully |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Auth required |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource not found |
| 500 | Server Error |

---

## 🧪 Quick Testing

### Using Swagger UI
1. Go to http://127.0.0.1:8000/swagger/
2. Find endpoint
3. Click "Try it out"
4. Fill parameters
5. Click "Execute"

### Using curl
```bash
# Get all books
curl http://127.0.0.1:8000/api/books/

# Search
curl "http://127.0.0.1:8000/api/search/?q=harry"

# Get statistics
curl http://127.0.0.1:8000/api/statistics/
```

---

## 💾 Sample Data

Run this command to load sample data:
```bash
python manage.py load_sample_data
```

**Includes:**
- 7 Authors
- 7 Genres  
- 7 Books
- 12 Reviews
- 5 Test Users

---

## 🎨 Data Models

### Book Fields
- `title` (required)
- `description`
- `isbn` (unique)
- `publisher`
- `publication_date`
- `page_count`
- `language`
- `author_ids` (array)
- `genre_ids` (array)

### Author Fields
- `name` (required)
- `biography`
- `birth_date`
- `nationality`

### Genre Fields
- `name` (required, unique)
- `description`

### Review Fields
- `book` (required, ID)
- `rating` (required, 1-5)
- `comment`

---

## 🚀 Quick Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Test API endpoints
curl http://127.0.0.1:8000/api/books/
```

---

## 📖 Documentation Links

- **Full API Docs:** `API_DOCUMENTATION.md`
- **README:** `README.md`
- **Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/

---

**Last Updated:** April 19, 2026
