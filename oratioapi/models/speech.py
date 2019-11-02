"""Module for for Speeches"""
from django.db import models
from django.contrib.auth.models import User


class Speech(models.Model):
    """Model class for ParkArea"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="speeches")
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    set_time = models.IntegerField(blank=True, null=True)
    actual_time = models.IntegerField(blank=True, null=True)
    transcript = models.CharField(max_length=500, blank=True, null=True)
    um = models.IntegerField(blank=True, null=True)
    uh = models.IntegerField(blank=True, null=True)
    like = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = ("speech")
        verbose_name_plural = ("speeches")

    def __str__(self):
        return self.transcript