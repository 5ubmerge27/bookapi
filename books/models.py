from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Author(models.Model):
    """作者模型"""
    name = models.CharField(max_length=200, verbose_name="作者姓名")
    biography = models.TextField(blank=True, verbose_name="作者简介")
    birth_date = models.DateField(null=True, blank=True, verbose_name="出生日期")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="国籍")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = "作者"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """图书分类模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称")
    description = models.TextField(blank=True, verbose_name="分类描述")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Book(models.Model):
    """图书模型"""
    title = models.CharField(max_length=300, verbose_name="书名")
    authors = models.ManyToManyField(Author, related_name='books', verbose_name="作者")
    genres = models.ManyToManyField(Genre, related_name='books', verbose_name="分类")
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True, verbose_name="ISBN")
    description = models.TextField(blank=True, verbose_name="图书描述")
    publication_date = models.DateField(null=True, blank=True, verbose_name="出版日期")
    publisher = models.CharField(max_length=200, blank=True, verbose_name="出版社")
    page_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="页数")
    language = models.CharField(max_length=50, default='English', verbose_name="语言")
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="平均评分"
    )
    ratings_count = models.PositiveIntegerField(default=0, verbose_name="评分数量")
    cover_image_url = models.URLField(blank=True, verbose_name="封面图片URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_rating(self):
        """更新平均评分"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = None
            self.ratings_count = 0
        self.save()


class Review(models.Model):
    """图书评论模型"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="图书")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="用户")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="评分"
    )
    comment = models.TextField(blank=True, verbose_name="评论内容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        unique_together = ('book', 'user')  # 每个用户对每本书只能评论一次
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 保存后更新图书的平均评分
        self.book.update_rating()


class ReadingList(models.Model):
    """阅读清单模型"""
    STATUS_CHOICES = [
        ('want_to_read', '想读'),
        ('currently_reading', '在读'),
        ('read', '已读'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists', verbose_name="用户")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_lists', verbose_name="图书")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='want_to_read', verbose_name="状态")
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "阅读清单"
        verbose_name_plural = "阅读清单"
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_status_display()})"
