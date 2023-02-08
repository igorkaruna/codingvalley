import logging

from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from whatchlists.models import Media
from notifications.models import Notification
from users.serializers import (ChangePasswordSerializer, UserSerializer, UserProfileSerializer,
                               RegisterSerializer, UpdateProfileSerializer,
                               UserTokenObtainPairSerializer)


logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    Implements logout on current session
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'users/logout: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """
    Implements logout on all devices
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.user.id
            tokens = OutstandingToken.objects.filter(user_id=user_id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'users/logout_all: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self, **kwargs):
        return User.objects.get(username=self.kwargs['username'])


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    Allows user to change password in profile settings
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class FollowView(APIView):
    """
    Follow user with notification to followed user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user = request.user
            to_user = User.objects.get(username=username)
            profile = to_user.userprofile
            if user == to_user:
                return Response('You can’ follow yourself', status=status.HTTP_400_BAD_REQUEST)

            if user in profile.followers.all():
                profile.followers.remove(user)
                profile.followers_count = profile.followers.count()
                profile.save()
                return Response('User unfollowed', status=status.HTTP_204_NO_CONTENT)
            else:
                profile.followers.add(user)
                profile.followers_count = profile.followers.count()
                profile.save()
                Notification.objects.create(
                    to_user=to_user,
                    created_by=user,
                    notification_type='follow',
                    followed_by=user,
                    content=f"{user.userprofile.user} started following you."
                )
                return Response('User followed', status=status.HTTP_200_OK)
        except Exception as e:
            message = {'detail': f'{e}'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class FavouritesView(APIView):
    """
    Follow user with notification to followed user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        try:
            media = Media.objects.get(id=uuid)
            profile = request.user.userprofile

            if media in profile.favourites.all():
                profile.favourites.remove(media)
                profile.favourites_count = profile.favourites.count()
                profile.save()
                return Response('Removed from favourites', status=status.HTTP_204_NO_CONTENT)
            else:
                profile.favourites.add(media)
                profile.favourites_count = profile.favourites.count()
                profile.save()
                return Response('Added to favourites', status=status.HTTP_200_OK)
        except Exception as e:
            message = {'detail': f'{e}'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)
