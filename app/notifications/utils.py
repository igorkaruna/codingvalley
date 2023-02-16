from notifications.models import Notification


def create_notification(to_user, created_by, notification_type, content):
    Notification.objects.create(
        to_user=to_user,
        created_by=created_by,
        notification_type=notification_type,
        content=content
    )
