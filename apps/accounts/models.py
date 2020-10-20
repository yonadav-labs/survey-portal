import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
    # Use a UUID for a primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User information
    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    middle_initial = models.CharField(_('middle initial'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone = models.CharField(max_length=16, blank=True, verbose_name='Phone number')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    # Account Validation
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('first_name', 'last_name', )
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = EmailUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_superuser
