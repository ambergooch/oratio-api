"""Module for for SpeechEvents"""
from django.db import models
from .speech import Speech
from .event import Event

class SpeechEvent(models.Model):
    """
    Creates the join table for the many to many relationship between speeches and events
    """
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("speechevent")
        verbose_name_plural = ("speechevent")


