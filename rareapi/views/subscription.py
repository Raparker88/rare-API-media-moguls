"""View module for handling requests about posttags"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Subscription, RareUser
from rest_framework.decorators import action

class Subscriptions(ViewSet):
    """Rare subscriptions"""

    def list(self, request):
        """Handle GET requests to get subscriptions by authed user; 
        needed for listing all subscribed posts on home"""

        subscriptions = Subscription.objects.all()

        #filtering subscriptions by user
        follower = RareUser.objects.get(user=request.auth.user)

        if follower is not None:
            subscriptions = subscriptions.filter(follower_id=follower)

        serializer = SubscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations; 
        will be used when user is on author profile and hits subscribe;
        only info needed in request is author ID"""

        follower = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk=request.data["author"])

        subscription = Subscription()
        subscription.follower = follower
        subscription.author = author

        if follower != author:
            try: 
                subscription.save()
                serializer = SubscriptionSerializer(subscription, context={'request': request})
                return Response(serializer.data)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"reason": "user cannot subscribe to their own posts"}, status=status.HTTP_400_BAD_REQUEST)

        @action(methods=['get'], detail=False)
        # Gets only active subscriptions (those without an ended_on) for the current user
        def get_current_subscriptions(self, request):
            follower = RareUser.objects.get(user=request.auth.user)

            if follower is not None:
                subscriptions = subscriptions.filter(follower_id=follower)
                subscriptions = subscriptions.filter(ended_on__isnull=True)

            serializer = SubscriptionSerializer(
                subscriptions, many=True, context={'request': request})
            return Response(serializer.data)
class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for subscription follower and author related Django user"""
    class Meta:
        model = RareUser
        fields = ('id', 'username')

class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for subscriptions"""
    follower = RareUserSerializer(many=False)
    author = RareUserSerializer(many=False)

    class Meta:
        model = Subscription
        url = serializers.HyperlinkedIdentityField(
            view_name='subscription',
            lookup_field='id'
        )
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')