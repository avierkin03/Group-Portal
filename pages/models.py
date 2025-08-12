from django.db import models
from django.contrib.auth.models import User

# Модель "Створінка", яка зберігає контент для статичних сторінок, включаючи головну
class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)   # зберігатиме "чистий" URL
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'