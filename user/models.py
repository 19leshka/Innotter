from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str = None, role: str = 'user') -> 'User':
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), role='admin')

        if role == 'admin':
            user.setAdminRole()

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(db_index=True, max_length=80, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def setAdminRole(self):
        self.role = self.Roles.ADMIN
