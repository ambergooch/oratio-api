from django.db import models
from .speech import Speech

class Prompt(models.Model):

    """
    Creates table for interview question prompts
    """
    prompt = models.TextField()

    class Meta:
        verbose_name = ("prompt")
        verbose_name_plural = ("prompts")

    def __str__(self):
        return self.question
