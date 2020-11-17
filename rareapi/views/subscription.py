"""View module for handling requests about posttags"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Subscription, RareUser

class Subscriptions(ViewSet):
    """Rare subscriptions"""

    def list(self, request):
        """Handle GET requests to get subscriptions by user"""

        subscriptions = Subscription.objects.all()

        #filtering subscriptions by user
        follower = RareUser.objects.get(user=request.auth.user)

        if follower is not None:
            subscriptions = subscriptions.filter(follower_id=follower)

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