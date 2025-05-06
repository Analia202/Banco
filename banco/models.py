# models.py
from django.db import models
from django.conf import settings

class CuentaBancaria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cuentas')
    numero = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.numero

class Cuenta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.numero} - {self.usuario.username}"

class Beneficiario(models.Model):
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
        ('transferencia', 'Transferencia'),
    ]
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    cuenta_destino = models.ForeignKey('Cuenta', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='movimientos_recibidos')

    def __str__(self):
        return f"{self.tipo} - {self.monto}"
