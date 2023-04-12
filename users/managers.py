from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        """
        Creates and saves a User with the given nickname and password.
        """
        if not nickname:
            raise ValueError('The nickname field must be set')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given nickname and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(nickname, password, **extra_fields)