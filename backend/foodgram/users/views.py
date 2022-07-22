from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SubscriptionSerializer, CustomUserSerializer
from .models import Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == 'subscribe':
            return SubscriptionSerializer
        return CustomUserSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response({
                'errors': 'You cannot subscribe on yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'You have already subscribed!'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Subscription.objects.create(user=user, author=author)
        serializer = self.get_serializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if user == author:
            return Response({
                'errors': 'You cannot unsubscribe yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Subscription.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'You have already unsubscribed!'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
