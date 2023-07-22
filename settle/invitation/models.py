from django.db import models
from settle.common.validators import only_letters
from django.core.validators import MinLengthValidator


class Invitation(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False, validators=[only_letters, MinLengthValidator(2)]
    )
    email = models.EmailField(
        max_length=50,
        null=False,
        blank=False,
    )
    location = models.TextField(
        max_length=300,
        null=False,
        blank=False,
    )
    date = models.DateField(
        null=False,
        blank=False,
    )
