from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.permissions import IsOwner
from discussions.models import Discussion, Comment
from discussions.serializers import (
    DiscussionSerializer, DiscussionSerializerForRetrieve,
    CommentSerializer, CommentSerializerForUpdate
)


class DiscussionViewSet(ModelViewSet):
    queryset = Discussion.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly | IsOwner | IsAdminUser]

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*5, key_prefix='discussions_viewset'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DiscussionSerializerForRetrieve
        return DiscussionSerializer


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly | IsOwner | IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return CommentSerializerForUpdate
        return CommentSerializer
