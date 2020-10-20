import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from apps.representatives.models import Representative


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password=None, is_superuser=False, **kwargs):
        user = self.model(email=email, is_superuser=is_superuser, **kwargs)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, is_superuser=False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, is_superuser=True, **kwargs)


class EmailUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField("Middle Initial", max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=16, blank=True, verbose_name='Phone number')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    date_joined = models.DateTimeField(default=timezone.now)
    representative = models.ForeignKey(Representative, on_delete=models.SET_NULL, blank=True, null=True)

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('first_name', 'last_name', )

    objects = EmailUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_superuser
