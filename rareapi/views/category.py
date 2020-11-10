"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class Categories(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all Categories

        Returns:
            Response -- JSON serialized list of Categories
        """
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='category',
            lookup_field='id'
        )
        fields = ('id', 'label')

"""Basic Serializer for single post"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
        depth = 1



