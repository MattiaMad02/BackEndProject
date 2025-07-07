from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='choices', null=True, blank=True)

    def __str__(self):
        return self.choice_text
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')  # <-- aggiungi related_name
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')
    def __str__(self):
        return f"{self.user} ha votato per {self.choice} nel sondaggio '{self.poll}'"