from django.db import models
from django.contrib.auth.models import User

# Модель "Портфоліо"
class PortfolioItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200, verbose_name='Назва проєкту')
    description = models.TextField(blank=True, verbose_name='Опис')
    screenshot = models.ImageField(upload_to='portfolio_screenshots/', blank=True, null=True, verbose_name='Скріншот')
    link = models.URLField(blank=True, null=True, verbose_name='Посилання')
    file = models.FileField(upload_to='portfolio_files/', blank=True, null=True, verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_public = models.BooleanField(default=False, verbose_name='Публічний проєкт')

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    class Meta:
        verbose_name = 'Проєкт портфоліо'
        verbose_name_plural = 'Проєкти портфоліо'