from django.contrib import admin
from .models import Cuenta, CuentaBancaria, Movimiento, Beneficiario

admin.site.register(Cuenta)
admin.site.register(CuentaBancaria)
admin.site.register(Movimiento)
admin.site.register(Beneficiario)
