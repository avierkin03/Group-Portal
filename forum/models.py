from django.db import models
from django.contrib.auth.models import User

# Модель "Теми форуму"
class ForumThread(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Forum Thread'
        verbose_name_plural = 'Forum Threads'


# Модель "Повідомлення в темах форуму"
class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.created_by.username} in {self.thread.title}"

    class Meta:
        verbose_name = 'Forum Post'
        verbose_name_plural = 'Forum Posts'