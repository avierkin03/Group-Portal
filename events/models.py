from django.db import models
from django.contrib.auth.models import User

# Модель "Подія"
class Event(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=256, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_date})"
