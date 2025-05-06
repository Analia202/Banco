from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class CIBackend(ModelBackend):
    def authenticate(self, request, ci=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(ci=ci)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None
