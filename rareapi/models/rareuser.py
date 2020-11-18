"""RareUser Model Module"""
from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    """RareUser Model"""
    bio = models.CharField(max_length=500)
    profile_image_url = models.ImageField(upload_to="images/", height_field=None, width_field=None, max_length=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    """This makes the username property accessible directly from the RareUser"""
    @property
    def username(self):
        return self.user.username

    """This makes the is_staff property accessible directly from the RareUser"""
    @property
    def is_staff(self):
        return self.user.is_staff

    """This makes the is_active property accessible directly from the RareUser"""
    @property
    def is_active(self):
        return self.user.is_active

    """This makes the email property accessible directly from the RareUser"""
    @property
    def email(self):
        return self.user.email

    """This makes the first and last name properties accessible directly from the RareUser as the full_name property"""
    @property
    def full_name(self):
        return (f'{self.user.first_name} {self.user.last_name}')

    """This makes the date_joined property accessible directly from the RareUser"""
    @property
    def date_joined(self):
        return self.user.date_joined

    """This unmapped property has a boolean value"""
    @property
    def is_current_user(self):
        return self.__is_current_user

    """This allows the is_current_user property to be set"""
    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value
