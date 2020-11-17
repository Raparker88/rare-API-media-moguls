"""View module for handling requests about reactions"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rareapi.models import Reaction, PostReaction, Post, RareUser

class Reactions(ViewSet):
    """rare reactions"""

    def list(self, request):
        """Handle GET requests to reactions resource

        Returns:
            Response -- JSON serialized list of reactions
        """
        reactions = Reaction.objects.all()

        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            for reaction in reactions:
                post_reactions = PostReaction.objects.filter(post_id=post_id)
                final_count = post_reactions.filter(reaction=reaction)
                reaction.count = len(final_count)


        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def react(self, request, pk=None):
        """Managing users reacting to posts"""

        if request.method == "POST":
            post = Post.objects.get(pk=request.data["post_id"])
            rareuser = RareUser.objects.get(user=request.auth.user)
            reaction = Reaction.objects.get(pk=pk)

            try:
                # Determine if the user already reacted
                like = PostReaction.objects.get(
                    post=post, user=rareuser, reaction=reaction)
                like.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
                
            except PostReaction.DoesNotExist:
                # The user is not signed up.
                like = PostReaction()
                like.post = post
                like.user = rareuser
                like.reaction = reaction
                like.save()

                return Response({}, status=status.HTTP_201_CREATED)

   

class ReactionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reactions

    Arguments:
        serializers
    """
    class Meta:
        model = Reaction
        fields = ('id', 'label', "image_url", 'count')