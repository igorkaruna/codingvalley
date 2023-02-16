from django.db import IntegrityError
from django.http import Http404
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from users.permissions import IsOwner
from reviews.models import Review, ReviewLikes
from reviews.serializers import ReviewSerializer, ReviewSerializerForUpdate, ReviewLikesSerializer


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly | IsOwner | IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return ReviewSerializerForUpdate
        return ReviewSerializer

    def get_serializer_context(self):
        context = {}
        context['request'] = self.request
        return context


class ReviewLikeViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    queryset = ReviewLikes.objects.all()
    serializer_class = ReviewLikesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly | IsOwner]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise Http404
