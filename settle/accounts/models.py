from enum import Enum

from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator


def validate_isalpha(value):
    return value.isalpha()


class SettleUser(auth_models.AbstractUser):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True,
    )
    profile_picture = models.URLField(
        null=True,
        blank=True,
    )
    spouse_first_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True,
    )
    spouse_last_name = models.CharField(
        max_length=30,
        validators=(MinLengthValidator(2), validate_isalpha),
        null=True,
        blank=True,
    )
    date_of_marriage = models.DateField(
        null=True,
        blank=True,
    )
