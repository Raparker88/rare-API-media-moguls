"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class Categories(ViewSet):
    """Rare categories"""

    def create(self, request):
        """Handle POST operations for categories"""

        category = Category()

        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CategorySerializer(serializers.HyperLinkedModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='category',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')