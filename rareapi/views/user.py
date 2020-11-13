"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rareapi.models import RareUser, Post
from rest_framework.decorators import action

class Users(ViewSet):
    """Users"""


    def list(self, request):
        """Handle GET requests to users resource

        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()


        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def posts(self, request):
        rareuser = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.filter(rareuser=rareuser)

        serializer = PostSerializer(posts, many=True, context={'request':request})
    def current_user(self, request):
        current_user = request.auth.user
        
        serializer = UserSerializer(current_user, context={'request': request})
        
        return Response(serializer.data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for rareusers

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active')

"""Serializer for RareUser Info in a post"""         
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'username', 'is_active', 'is_staff', 'email', 'full_name')

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    rareuser = PostRareUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'content', 'rareuser', 'category', 'approved')
        depth = 1
        fields = ('username', 'is_staff', 'is_active', 'email', 'date_joined', 'first_name', 'last_name')
