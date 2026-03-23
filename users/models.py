from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ["email", "age"]
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        null=False,
        blank=False,
    )
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username