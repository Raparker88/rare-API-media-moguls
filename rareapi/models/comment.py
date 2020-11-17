"""Comment Model Module"""
from django.db import models

class Comment(models.Model):
    """Comment Model"""
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def is_user_author(self):
        return self.__is_user_author

    @is_user_author.setter
    def is_user_author(self, value):
        self.__is_user_author = value
    