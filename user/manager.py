from django.contrib.auth.base_user import BaseUserManager

from .enum import Roles


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str = None, role: str = Roles.USER, image: str = None) -> 'User':
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), role=role, image=image)

        if role == 'admin':
            user.setAdminRole()

        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password, role=Roles.ADMIN.value)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


