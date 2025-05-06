# usuarios/urls.py
from django.urls import path
from .views import RegistroView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('token/', LoginView.as_view(), name='login'),
    path('token/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
