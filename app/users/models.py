import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from whatchlists.models import Media
from users.utils import generate_username
from users.managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    username = models.CharField(default=generate_username, max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE, primary_key=True
    )
    bio = models.TextField(default=None, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name="following", blank=True)
    favourites = models.ManyToManyField(Media, related_name="users", blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
