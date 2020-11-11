"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for rareusers

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active')