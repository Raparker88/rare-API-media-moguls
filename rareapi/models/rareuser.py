"""RareUser Model Module"""
from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    """RareUser Model"""
    bio = models.CharField(max_length=500)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return (f'{self.user.first_name} {self.user.last_name}')