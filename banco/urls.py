# banco/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuentaViewSet, MovimientoViewSet, BeneficiarioViewSet

router = DefaultRouter()
router.register(r'cuentas', CuentaViewSet, basename='cuenta')
router.register(r'movimientos', MovimientoViewSet, basename='movimiento')
router.register(r'beneficiarios', BeneficiarioViewSet, basename='beneficiario')

urlpatterns = [
    path('', include(router.urls)),
]
