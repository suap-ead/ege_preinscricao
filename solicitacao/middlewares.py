
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import get_object_or_404
from .models import Selecionado


class SelecionadoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        selecionado_id = request.session.get("selecionado_id", None)
        if selecionado_id:
            request.selecionado = get_object_or_404(Selecionado, id=selecionado_id)
