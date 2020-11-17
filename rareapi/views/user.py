"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rareapi.models import RareUser, Post
from rest_framework.decorators import action
from rareapi.views.category import CategorySerializer

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

    def retrieve(self, request, pk=None):
        """Handle GET request for single user for User Profile View
        Returns:
            Response -- JSON serielized rareuser instance
        """
        try:
            rareuser = RareUser.objects.get(pk=pk)

            rareuser.is_current_user = None
            current_rareuser = RareUser.objects.get(user=request.auth.user)

            if current_rareuser.id == int(pk):
                rareuser.is_current_user = True
            else:
                rareuser.is_current_user = False

            rareuser = RareUserSerializer(rareuser, many=False, context={'request': request})

            return Response(rareuser.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['get'], detail=False)
    def posts(self, request):
        rareuser = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.filter(rareuser=rareuser)

        serializer = PostSerializer(posts, many=True, context={'request': request})

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def current_user(self, request):
        current_user = request.auth.user

        serializer = UserSerializer(current_user, context={'request': request})

        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    def change_type(self, request, pk=None):
        user_obj = User.objects.get(pk=pk)

        user_obj.is_staff = not user_obj.is_staff
        user_obj.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for rareusers
    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id','username', 'is_staff', 'is_active', 'first_name', 'last_name', 'email', 'date_joined')

"""Serializer for RareUser Info in a post"""
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'username', 'is_active', 'is_staff', 'email', 'full_name')

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    rareuser = PostRareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'content', 'rareuser', 'category', 'rareuser_id', 'is_user_author', 'approved')
        depth = 1

"""Serializer for RareUser info in profile detail view"""
class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ("id", "bio", "is_staff", "is_active", "full_name", "profile_image_url", "is_current_user", "username", "email", "date_joined")
