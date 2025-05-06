# serializers.py
from rest_framework import serializers
from .models import CuentaBancaria , Cuenta, Movimiento, Beneficiario

class CuentaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaBancaria
        fields = ['id', 'numero', 'saldo']
class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['id', 'numero', 'saldo']

class BeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiario
        fields = ['id', 'nombre', 'numero_cuenta']

    def validate_numero_cuenta(self, value):
        user = self.context['request'].user

        # Validar que no se duplique con el mismo usuario
        if Beneficiario.objects.filter(usuario=user, numero_cuenta=value).exists():
            raise serializers.ValidationError("Ya registraste un beneficiario con este número de cuenta.")

        # Validar que el número de cuenta exista realmente
        if not Cuenta.objects.filter(numero=value).exists():
            raise serializers.ValidationError("El número de cuenta indicado no existe en el sistema.")

        return value
class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id', 'cuenta', 'tipo', 'monto', 'fecha', 'descripcion', 'cuenta_destino']
