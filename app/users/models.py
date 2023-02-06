import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from users.managers import UserManager
from users.utils import generate_username


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(
        default=generate_username,
        max_length=50,
        unique=True
    )
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    bio = models.TextField(default=None, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    favourites = models.ManyToManyField(Media, related_name="users", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_username(self):
        return self.username

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def get_email(self):
        return self.email
