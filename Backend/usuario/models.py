from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    legajo = models.IntegerField(unique=True,
                            validators=[MinValueValidator(0, message='Inserte un legajo válido')],
                            null=True)
    cargo = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=255, null=True)
    default_password = models.BooleanField(default=True)

    def is_active_(self, raise_exception=False):
        if not self.is_active:
            if raise_exception:
                raise ObjectDoesNotExist("Objeto no existe")
            return False
        return True
