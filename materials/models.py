from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse, parse_qs

# Модель "Навчальний матеріал"
class Material(models.Model):
    CONTENT_TYPES = [
        ('file', 'Файл'),
        ('image', 'Зображення'),
        ('youtube', 'YouTube-відео'),
    ]

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='materials/files/', blank=True, null=True)
    image = models.ImageField(upload_to='materials/images/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="materials")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # парсить ID з YouTube-URL для embed
    def get_youtube_id(self):
        # Перевіряємо, чи тип контенту 'youtube' і чи є URL
        if self.content_type == 'youtube' and self.youtube_url:
            # Розбираємо URL на компоненти (схема, хост, шлях, параметри тощо)
            parsed_url = urlparse(self.youtube_url)

            # Якщо це короткий URL (youtu.be), ID беремо з шляху (path) після першого слеша
            if parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]
            
            # Якщо це стандартний YouTube-URL (youtube.com або www.youtube.com)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                # Для формату /watch?v=ID (наприклад, /watch?v=dQw4w9WgXcQ)
                if parsed_url.path == '/watch':
                    # Витягуємо параметр 'v' із query-рядка (наприклад, v=dQw4w9WgXcQ)
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                
                # Для формату /embed/ID (наприклад, /embed/dQw4w9WgXcQ)
                if parsed_url.path[:7] == '/embed/':
                    return parsed_url.path.split('/')[2]
                
                # Для формату /v/ID (старий формат, наприклад, /v/dQw4w9WgXcQ)
                if parsed_url.path[:3] == '/v/':
                    return parsed_url.path.split('/')[2]
        return None