from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from .validators import validate_file_size

UserModel = get_user_model()


class Photo(models.Model):
    title = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )
    photo = models.ImageField(
        upload_to='images',
        validators=(
            validate_file_size,
        )
    )
    description = models.TextField(
        max_length=200,
        validators=(
            MinLengthValidator(10),
        ),
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    date_of_publication = models.DateField(
        auto_now=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
