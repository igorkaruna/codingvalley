from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class GetNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_read = request.query_params.get('is_read')
        if not is_read:
            notifications = request.user.notifications.order_by('-created')
        else:
            notifications = request.user.notifications.filter(is_read=is_read).order_by('-created')

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class ReadNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        try:
            if (notification := Notification.objects.get(id=uuid)).to_user == request.user:
                notification.delete()
                return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Something went wrong, please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'details': f'{e}'}, status=status.HTTP_204_NO_CONTENT)
