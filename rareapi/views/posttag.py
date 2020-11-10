"""View module for handling requests about posttags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import PostTag, Tag, Post

class PostTags(ViewSet):
    """Rare post tags"""

    def list(self, request):
        """Handle GET requests to get posttags by post"""

        posttags = PostTag.objects.all()

        #filtering posttags by post
        post = self.request.query_params.get("postId", None)

        if post is not None:
            posttags = posttags.filter(post_id=post)

        serializer = PostTagSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)

class PostTagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posttags
    Arguments:
        serializer type
    """

    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id')