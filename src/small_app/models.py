import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models

from .managers import UserManager, PassportManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'username': self.username,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Passport(models.Model):

    first_name = models.CharField(db_index=True, max_length=255, null=False)
    last_name = models.CharField(db_index=True, max_length=255, null=False)
    passport_series = models.SmallIntegerField(null=False)
    passport_number = models.SmallIntegerField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    objects = PassportManager()

    def __str__(self):
        return self.first_name + self.last_name
