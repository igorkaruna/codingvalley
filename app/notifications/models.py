import uuid

from django.contrib.auth import get_user_model
from django.db import models


CHOICES = (
    ('follow', 'follow'),
)


class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='notifications',)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    content = models.CharField(max_length=255)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content
