"""Category Model Module"""
from django.db import models

class Category(models.Model):
    """Category Model"""
    label = models.CharField(max_length=25)
