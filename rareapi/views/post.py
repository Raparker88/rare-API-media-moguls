from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Post, RareUser

class Posts(ViewSet):
    def list(self, request):

        posts = Post.objects.all()

        rareuser_id = self.request.query_params.get('rareuser_id', None)
        if rareuser_id is not None:
            posts = posts.filter(rareuser_id=rareuser_id)
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET request for single post
        Returns:
            Response JSON serielized post instance
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            

"""Serializer for RareUser Info in a post"""         
class PostRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'username', 'is_active', 'is_staff', 'email')

"""Basic Serializer for single post"""
class PostSerializer(serializers.ModelSerializer):
    rareuser = PostRareUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'content', 'rareuser', 'category')
        depth = 1