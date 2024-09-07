from django.core.validators import MinLengthValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.name
