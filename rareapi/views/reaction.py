"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Reaction

class Reactions(ViewSet):
    """rare reactions"""

    def list(self, request):
        """Handle GET requests to reactions resource

        Returns:
            Response -- JSON serialized list of reactions
        """
        reactions = Reaction.objects.all()


        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request})
        return Response(serializer.data)

   

class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', "image_url")