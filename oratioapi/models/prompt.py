from django.db import models
from .speech import Speech

class Prompt(models.Model):

    """
    Creates table for interview question prompts
    """
    question = models.CharField(max_length = 55)
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE, related_name="prompt")

    class Meta:
        verbose_name = ("prompt")
        verbose_name_plural = ("prompts")

    def __str__(self):
        return self.question
