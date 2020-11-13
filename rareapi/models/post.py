"""Post Model Module"""
from django.db import models

class Post(models.Model):
    """Post Model"""
    rareuser = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    image_url = models.ImageField()
    content = models.CharField(max_length=5000)
    approved = models.BooleanField()

    @property
    def is_user_author(self):
        return self.__is_user_author

    @is_user_author.setter
    def is_user_author(self, value):
        self.__is_user_author = value
