from django.db import models
from django.contrib.auth.models import User

# Модель "Голосування"
class Vote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'


# Модель "Варіанти відповідей для голосування"
class VoteOption(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.vote.title}: {self.text}"

    class Meta:
        verbose_name = 'Vote Option'
        verbose_name_plural = 'Vote Options'


# Модель "Голос користувача"
class UserVote(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='user_votes')
    option = models.ForeignKey(VoteOption, on_delete=models.CASCADE, related_name='user_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} voted in {self.vote.title}"

    class Meta:
        verbose_name = 'User Vote'
        verbose_name_plural = 'User Votes'
        unique_together = ['vote', 'user']  # Один голос на користувача для голосування