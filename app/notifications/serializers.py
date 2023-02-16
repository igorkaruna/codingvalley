from rest_framework import serializers

from users.serializers import UserProfileSerializer
from reviews.serializers import ReviewSerializer
from notifications.models import Notification
from discussions.serializers import DiscussionSerializer


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
