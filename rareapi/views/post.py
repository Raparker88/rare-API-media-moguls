from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Post, RareUser, Category, PostTag

class Posts(ViewSet):
    def create(self, request):
        """Handle POST operations for posts"""

        rareuser = RareUser.Objects.get(user=request.auth.user)
        category = Category.Objects.get(pk=request.data["category_id"])

        post = Post()

        post.category = category
        post.raruser = rareuser
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
            #iterate selected categories and save to database
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

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            posts = posts.filter(user_id=user_id)
        
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