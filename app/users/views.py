import logging

import requests

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.managers import UserManager
from users.models import User
from notifications.utils import create_notification
from users.serializers import (ChangePasswordSerializer, RegisterSerializer,
                               UpdateProfileSerializer, UserSerializer,
                               UserTokenObtainPairSerializer)
from watchlists.models import Media


logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    Logout user from current session
    using blacklist RefreshToken method.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'LogoutView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """
    Logout user from all sessions
    using blacklist OutstandigToken method.
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
            logger.error(f'LogoutAllView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = {'access_token': request.data.get('token')}
        request = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        if 'error' in (data := json.loads(request.text)):
            return Response({'detail': 'Wrong google token or already expired.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.email = data['email']
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            user.email_verified = True
            user.password = make_password(UserManager().make_random_password())
            user.save()

        token = RefreshToken.for_user(user)
        response = {}
        response['email'] = user.email
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response, status=status.HTTP_302_FOUND)


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60*1, key_prefix='userprofile_cache'))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self, **kwargs):
        return User.objects.get(username=self.kwargs['username'])


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60*1, key_prefix='to_userprofile_cache'))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self, **kwargs):
        return User.objects.get(username=self.kwargs['username'])


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user = request.user
            to_user = User.objects.get(username=username)
            if user == to_user:
                return Response({'detail': 'You can’t follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

            to_userprofile = to_user.userprofile
            if to_userprofile.followers.filter(username=user.username).exists():
                to_userprofile.followers.remove(user)
                to_userprofile.save()
                return Response({'detail': f'You stop following {to_user}'}, status=status.HTTP_204_NO_CONTENT)

            to_userprofile.followers.add(user)
            to_userprofile.save()
            create_notification(
                to_user=to_user,
                created_by=user,
                notification_type='follow',
                content=f"{user.userprofile.user} started following you."
            )
            return Response({'detail': f'You start following {to_user}'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'FollowView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class AddFavouritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        try:
            userprofile = request.user.userprofile
            media = Media.objects.get(id=uuid)
            if userprofile.favourites.filter(id=media.id).exists():
                userprofile.favourites.remove(media)
                userprofile.save()
                return Response({'detail': f'{media} was removed from favourites.'}, status=status.HTTP_204_NO_CONTENT)

            userprofile.favourites.add(media)
            userprofile.save()
            return Response({'detail': f'{media} was added to favourites.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'FavouritesView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.email_verified:
            return Response({'detail': 'Your email is already activated.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            title = 'Verify your Valley account'
            message = render_to_string('verify-email.html', {
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMultiAlternatives(title, message, to=[user.email])
            email.attach_alternative(message, 'text/html')
            email.send()
            return Response({'detail': f'Email with activation link was sent to {user.email}'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'SendEmailView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_403_FORBIDDEN)


class ActivateEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            logger.error(f'Error with activation: {e}')

        if not default_token_generator.check_token(user, token) or user is None:
            return Response({'detail': 'Something went wrong, please try again.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if user.email_verified:
            return Response({'detail': f'Bad request. {user.email} already activated.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user.email_verified = True
        user.save()
        return Response({'detail': f'{user.email} was successfuly activated.'}, status=status.HTTP_200_OK)


class ResetSendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        user_email = data.get('email')
        user = User.objects.get(email=user_email)
        try:
            title = f'Reset passowrd for {user.username}'
            message = render_to_string('reset-email.html', {
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMultiAlternatives(title, message, to=[user.email])
            email.attach_alternative(message, 'text/html')
            email.send()
            return Response({'detail': f'Email with reset link was sent to {user.email}'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'ResetEmailView: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            logger.error(f'ResetPasswordView {e}')
            user = None

        if user is None:
            return Response({'detail': 'Something went wrong, please try again.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Something went wrong, please try again.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        new_password = request.data.get('new_password')
        if new_password != request.data.get('new_password2'):
            return Response({'detail': 'Password doesn’t match'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user.set_password(new_password)
        user.save()
        return Response('Your password was reset successfuly!')
