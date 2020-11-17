"""View module for handling requests about posttags"""
import datetime
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
        author = RareUser.objects.get(pk=request.data["author_id"])

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
        subscriptions = Subscription.objects.all()
        follower = RareUser.objects.get(user=request.auth.user)

        if follower is not None:
            subscriptions = subscriptions.filter(follower_id=follower, ended_on__isnull=True)

        serializer = SubscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['patch'], detail=True)
    # Adds an ended_on for an active subscription between a follower and author
    def unsubscribe(self, request, pk=None):
        subscription_obj = Subscription.objects.get(pk=pk)

        subscription_obj.ended_on = datetime.datetime.now()
        subscription_obj.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    # Gets only active subscriptions (those without an ended_on) for the current user
    # AND  a given author
    # Used to indicate on author's profile page whether user has a current subscription to the author
    # Will also be used on front end to make SURE sure before creating a subscription that an active one doesn't already exist
    def get_single_current_subscription(self, request):
        subscriptions = Subscription.objects.all()
        follower = RareUser.objects.get(user=request.auth.user)
        author = RareUser.objects.get(pk=request.data["author_id"])

        if follower is not None:
            subscriptions = subscriptions.filter(follower_id=follower, ended_on__isnull=True, author=author)

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