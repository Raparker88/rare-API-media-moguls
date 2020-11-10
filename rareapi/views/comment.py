"""View module for handling requests about comments"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser, Post


class Comments(ViewSet):
    """Rare comments"""

    def create(self, request):

        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["postId"])

        comment = Comment()
        comment.post = post
        comment.author = author
        comment.content = request.data["content"]
        comment.subject = request.data["subject"]

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to comments resource

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        # Support filtering events by game
        post = self.request.query_params.get('postId', None)
        if post is not None:
            comments = comments.filter(post__id=post)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for post author's related Django user"""
    class Meta:
        model = RareUser
        fields = ['username']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for post"""
    class Meta:
        model = Post
        fields = ('id')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for comments"""
    author = CommentAuthorSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = Comment
        url = serializers.HyperlinkedIdentityField(
            view_name='comment',
            lookup_field='id'
        )
        fields = ('id', 'url', 'post', 'author',
                'content', 'subject', 'created_on')
# Ready for postman testing once data is loaded