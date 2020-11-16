"""Subscription Model Module"""
from django.db import models

class Subscription(models.Model):
    """Subscription Model"""
    follower_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='follower_id')
    author_id = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='author_id')
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True)