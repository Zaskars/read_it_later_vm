from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from web.enums import Role


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=Role.choices,
        max_length=15,
        default=Role.user
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    telegram_user_id = models.PositiveIntegerField(verbose_name="Telegram user ID", unique=True, null=True, blank=True)

    @property
    def is_staff(self):
        return self.role in (Role.admin, Role.staff)

    @property
    def is_superuser(self):
        return self.role == Role.admin

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Articles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    is_archived = models.BooleanField()
    document_file = models.FileField(null=True, upload_to='articles/')


class Tags(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)


class TelegramHash(models.Model):
    hash = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
