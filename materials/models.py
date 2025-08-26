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
        if self.content_type == 'youtube' and self.youtube_url:
            parsed_url = urlparse(self.youtube_url)
            if parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                if parsed_url.path[:7] == '/embed/':
                    return parsed_url.path.split('/')[2]
                if parsed_url.path[:3] == '/v/':
                    return parsed_url.path.split('/')[2]
        return None