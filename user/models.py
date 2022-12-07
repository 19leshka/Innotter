from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from user.enum import Roles
from user.manager import UserManager


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=80, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices(), default=Roles.USER.value)
    title = models.CharField(max_length=80, blank=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def setAdminRole(self):
        self.role = self.Roles.ADMIN
