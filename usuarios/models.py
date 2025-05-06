# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True)
    numero_cuenta = models.CharField(max_length=20, unique=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre_completo', 'ci']

    def save(self, *args, **kwargs):
        if not self.numero_cuenta:
            self.numero_cuenta = self.generar_numero_cuenta()
        super().save(*args, **kwargs)

    def generar_numero_cuenta(self):
        return str(uuid.uuid4().int)[:10]

    def __str__(self):
        return self.username
