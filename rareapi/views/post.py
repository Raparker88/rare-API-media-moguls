from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rareapi.models import Post, RareUser, Category, PostTag

class Posts(ViewSet):
    def create(self, request):
        """Handle POST operations for posts"""

        rareuser = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category_id"])

        post = Post()

        post.category = category
        post.rareuser = rareuser
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.selected_tags = request.data["selected_tags"]

        if rareuser.is_staff:
            post.approved = True
        else:
            post.approved = False

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            #iterate selected tags and save relationships to database
            for tag in post.selected_tags:

                posttag = PostTag()
                posttag.tag_id = int(tag["id"])
                posttag.post_id = int(serializer.data["id"])
                
                posttag.save()
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
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
    
    def update(self, request, pk=None):
        """Handle PUT requests for posts"""

        rareuser = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.content = request.data["content"]
        post.selected_tags = request.data["selected_tags"]
        post.rareuser = rareuser

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.save()

        serializer = PostSerializer(post, context={'request': request})
            #iterate selected tags and save relationships to database
        for tag in post.selected_tags:

            posttag = PostTag()
            posttag.tag_id = int(tag["id"])
            posttag.post_id = int(serializer.data["id"])
            
            posttag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
        
            

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