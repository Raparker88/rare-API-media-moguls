"""RareUser Model Module"""
from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    """RareUser Model"""
    bio = models.CharField(max_length=500)
    profile_img_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateField()
    active = models.BooleanField()
