from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, email, password, email_verified, is_superuser, is_staff, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            email_verified=email_verified,
            is_superuser=is_superuser,
            is_staff=is_staff,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        user = self._create_user(first_name, last_name, email, password, False, False, False, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        user = self._create_user(first_name, last_name, email, password, True, True, True, **extra_fields)
        user.save(using=self._db)
        return user
