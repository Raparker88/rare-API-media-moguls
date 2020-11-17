"""Reaction Model Module"""
from django.db import models

class Reaction(models.Model):
    """Reaction Model"""
    label = models.CharField(max_length=25)
    image_url = models.ImageField(upload_to="emojis/")