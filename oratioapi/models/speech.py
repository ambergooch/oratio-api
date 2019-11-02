"""Module for for Speeches"""
from django.db import models
from django.contrib.auth.models import User
from .prompt import Prompt


class Speech(models.Model):
    """Model class for ParkArea"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="speeches")
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="speech")
    set_time = models.IntegerField(blank=True, null=True)
    actual_time = models.IntegerField(blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    um = models.IntegerField(blank=True, null=True)
    uh = models.IntegerField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = ("speech")
        verbose_name_plural = ("speeches")

    def __str__(self):
        return self.transcript