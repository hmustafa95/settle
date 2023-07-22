from django.db import models
from django.core.validators import MinLengthValidator
from .validators import only_letters, only_digits


class Subscribe(models.Model):
    email = models.EmailField(
        max_length=50,
        null=False,
        blank=False,
    )


class Contact(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False, validators=[only_letters, MinLengthValidator(2)]
    )
    phone = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        validators=[MinLengthValidator(6), only_digits]
    )
    email = models.EmailField(
        max_length=50,
        null=False,
        blank=False,
    )
    message = models.TextField(
        max_length=300,
        null=False,
        blank=False,
    )
