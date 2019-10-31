"""Module for Events"""
from django.db import models

class Event(models.Model):
    """Model class for Events"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("event")
        verbose_name_plural = ("events")

    def __str__(self):
        return self.name