from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, email, password, email_verified, is_admin, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            email_verified=email_verified,
            is_admin=is_admin,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        user = self._create_user(
            first_name, last_name, email, password,
            False, False, **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        user = self._create_user(
            first_name, last_name, email, password,
            True, True, **extra_fields
        )
        user.save(using=self._db)
        return user
