"""
URL configuration for bookapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from django.http import HttpResponse

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Book Metadata and Recommendation API",
        default_version='v1.0',
        description="""
        A comprehensive book management REST API providing the following features:
        - Complete CRUD operations for books
        - Author management
        - Genre classification
        - Rating and review system
        - Full-text search functionality
        - Intelligent recommendation algorithm
        - Statistical analysis
        
        Tech Stack: Django 6.0.3 + Django REST Framework + SQLite
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def api_root(request):
    """API root endpoint providing information about all available endpoints"""
    # Return JSON if Accept header contains application/json
    if request.META.get('HTTP_ACCEPT', '').find('application/json') != -1:
        from rest_framework.response import Response
        return Response({
            'message': 'Welcome to Book Metadata and Recommendation API',
            'version': '1.0',
            'endpoints': {
                'authors': '/api/authors/',
                'genres': '/api/genres/',
                'books': '/api/books/',
                'reviews': '/api/reviews/',
                'reading_list': '/api/reading-list/',
                'search': '/api/search/?q=<query>',
                'popular_books': '/api/popular/',
                'statistics': '/api/statistics/',
                'recommendations': '/api/books/<id>/recommendations/',
                'admin': '/admin/',
            }
        })
    
    # Otherwise return HTML page
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book Metadata and Recommendation API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 15px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 40px;
                font-size: 1.2em;
            }
            .endpoints {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .endpoint {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .endpoint:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }
            .endpoint h3 {
                margin: 0 0 10px 0;
                color: #495057;
                font-size: 1.3em;
            }
            .endpoint a {
                color: #007bff;
                text-decoration: none;
                font-family: monospace;
                background: #e9ecef;
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
                margin-top: 10px;
            }
            .endpoint a:hover {
                background: #007bff;
                color: white;
            }
            .stats {
                background: #e8f5e8;
                border-radius: 10px;
                padding: 20px;
                margin: 30px 0;
                text-align: center;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 0.8em;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .put { background: #ffc107; color: black; }
            .delete { background: #dc3545; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Book API</h1>
            <p class="subtitle">Book Metadata and Recommendation API System</p>
            
            <div class="stats">
                <h3>🚀 API Status: Running</h3>
                <p>Version: 1.0 | Database: SQLite | Framework: Django REST Framework</p>
            </div>

            <div class="endpoints">
                <div class="endpoint">
                    <h3>📖 Book Management</h3>
                    <p>Manage book information with full CRUD operations</p>
                    <span class="method get">GET</span><span class="method post">POST</span>
                    <a href="/api/books/" target="_blank">/api/books/</a>
                    <br>
                    <span class="method get">GET</span><span class="method put">PUT</span><span class="method delete">DELETE</span>
                    <a href="/api/books/1/" target="_blank">/api/books/{id}/</a>
                </div>

                <div class="endpoint">
                    <h3>👤 Author Management</h3>
                    <p>Manage author information and works</p>
                    <span class="method get">GET</span><span class="method post">POST</span>
                    <a href="/api/authors/" target="_blank">/api/authors/</a>
                    <br>
                    <span class="method get">GET</span><span class="method put">PUT</span><span class="method delete">DELETE</span>
                    <a href="/api/authors/1/" target="_blank">/api/authors/{id}/</a>
                </div>

                <div class="endpoint">
                    <h3>🏷️ Genre Management</h3>
                    <p>Manage book genres and categories</p>
                    <span class="method get">GET</span><span class="method post">POST</span>
                    <a href="/api/genres/" target="_blank">/api/genres/</a>
                    <br>
                    <span class="method get">GET</span><span class="method put">PUT</span><span class="method delete">DELETE</span>
                    <a href="/api/genres/1/" target="_blank">/api/genres/{id}/</a>
                </div>

                <div class="endpoint">
                    <h3>⭐ Review System</h3>
                    <p>User ratings and review management</p>
                    <span class="method get">GET</span><span class="method post">POST</span>
                    <a href="/api/reviews/" target="_blank">/api/reviews/</a>
                    <br>
                    <span class="method get">GET</span><span class="method put">PUT</span><span class="method delete">DELETE</span>
                    <a href="/api/reviews/1/" target="_blank">/api/reviews/{id}/</a>
                </div>

                <div class="endpoint">
                    <h3>🔍 Search</h3>
                    <p>Full-text search across books, authors, and genres</p>
                    <span class="method get">GET</span>
                    <a href="/api/search/?q=harry" target="_blank">/api/search/?q={query}</a>
                </div>

                <div class="endpoint">
                    <h3>🔥 Popular Books</h3>
                    <p>Top-rated books sorted by rating</p>
                    <span class="method get">GET</span>
                    <a href="/api/popular/" target="_blank">/api/popular/</a>
                </div>

                <div class="endpoint">
                    <h3>🤖 Smart Recommendations</h3>
                    <p>Content-based book recommendation algorithm</p>
                    <span class="method get">GET</span>
                    <a href="/api/books/1/recommendations/" target="_blank">/api/books/{id}/recommendations/</a>
                </div>

                <div class="endpoint">
                    <h3>📊 Statistics</h3>
                    <p>System statistics and data analysis</p>
                    <span class="method get">GET</span>
                    <a href="/api/statistics/" target="_blank">/api/statistics/</a>
                </div>

                <div class="endpoint">
                    <h3>📋 Reading List</h3>
                    <p>Personal reading list management</p>
                    <span class="method get">GET</span><span class="method post">POST</span>
                    <a href="/api/reading-list/" target="_blank">/api/reading-list/</a>
                </div>

                <div class="endpoint">
                    <h3>⚙️ Admin Panel</h3>
                    <p>Django administration interface</p>
                    <span class="method get">GET</span>
                    <a href="/admin/" target="_blank">/admin/</a>
                </div>
            </div>

            <div style="margin-top: 40px; text-align: center;">
                <a href="/swagger/" style="display: inline-block; padding: 15px 30px; background: #85ea2d; color: black; text-decoration: none; border-radius: 8px; font-size: 1.1em; margin: 10px; font-weight: bold;">
                    📖 Swagger UI Documentation
                </a>
                <a href="/redoc/" style="display: inline-block; padding: 15px 30px; background: #8c54ff; color: white; text-decoration: none; border-radius: 8px; font-size: 1.1em; margin: 10px;">
                    📚 ReDoc Documentation
                </a>
                <div style="margin-top: 20px; color: #666;">
                    <p>💡 Swagger UI provides interactive API documentation and testing | ReDoc offers beautiful documentation display</p>
                    <p>📚 Course Project: Web Services and Web Data (XJCO3011)</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('books.urls')),
    
    # Swagger UI Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path("", api_root, name='api-root'),
]
