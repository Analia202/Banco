from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, permissions, serializers
from .models import CuentaBancaria, Cuenta, Movimiento, Beneficiario
from .serializers import (
    CuentaBancariaSerializer,
    CuentaSerializer,
    MovimientoSerializer,
    BeneficiarioSerializer
)


class CuentaBancariaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cuentas = CuentaBancaria.objects.filter(usuario=request.user)
        serializer = CuentaBancariaSerializer(cuentas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CuentaBancariaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuentaViewSet(viewsets.ModelViewSet):
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cuenta.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Movimiento.objects.filter(cuenta__usuario=self.request.user)
        cuenta_id = self.request.query_params.get('cuenta')
        if cuenta_id:
            queryset = queryset.filter(cuenta_id=cuenta_id)
        return queryset

    def perform_create(self, serializer):
        tipo = self.request.data.get('tipo')  # "ingreso", "egreso" o "transferencia"
        monto = Decimal(str(self.request.data.get('monto')))
        cuenta_id = self.request.data.get('cuenta')
        cuenta = Cuenta.objects.filter(id=cuenta_id, usuario=self.request.user).first()

        if not cuenta:
            raise serializers.ValidationError("La cuenta no pertenece al usuario autenticado.")

        if tipo == 'ingreso':
            cuenta.saldo += monto
            cuenta.save()
            serializer.save(cuenta=cuenta)

        elif tipo == 'egreso':
            if cuenta.saldo < monto:
                raise serializers.ValidationError("Saldo insuficiente.")
            cuenta.saldo -= monto
            cuenta.save()
            serializer.save(cuenta=cuenta)

        elif tipo == 'transferencia':
            cuenta_destino_numero = self.request.data.get('cuenta_destino')
            cuenta_destino = Cuenta.objects.filter(numero=cuenta_destino_numero).first()

            if not cuenta_destino:
                raise serializers.ValidationError("Cuenta destino no encontrada.")

            if cuenta.saldo < monto:
                raise serializers.ValidationError("Saldo insuficiente.")

            # Transferencia a cuenta propia
            if cuenta_destino.usuario == self.request.user:
                cuenta.saldo -= monto
                cuenta_destino.saldo += monto
                cuenta.save()
                cuenta_destino.save()

                # Movimiento origen
                serializer.save(
                    cuenta=cuenta,
                    cuenta_destino=cuenta_destino,
                    descripcion=f'Transferencia a cuenta propia {cuenta_destino.numero}'
                )

                # Movimiento espejo
                Movimiento.objects.create(
                    cuenta=cuenta_destino,
                    tipo='ingreso',
                    monto=monto,
                    descripcion=f'Transferencia recibida de tu cuenta {cuenta.numero}'
                )

            else:
                # Validamos si esa cuenta está registrada como beneficiario
                beneficiario_ok = Beneficiario.objects.filter(
                    numero_cuenta=cuenta_destino.numero
                ).exists()

                if not beneficiario_ok:
                    raise serializers.ValidationError("El beneficiario no está registrado.")

                cuenta.saldo -= monto
                cuenta_destino.saldo += monto
                cuenta.save()
                cuenta_destino.save()

                serializer.save(
                    cuenta=cuenta,
                    cuenta_destino=cuenta_destino,
                    descripcion=f'Transferencia a tercero {cuenta_destino.numero}'
                )

                Movimiento.objects.create(
                    cuenta=cuenta_destino,
                    tipo='ingreso',
                    monto=monto,
                    descripcion=f'Transferencia recibida de {cuenta.numero}'
                )

class BeneficiarioViewSet(viewsets.ModelViewSet):
    serializer_class = BeneficiarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Beneficiario.objects.all()
