import json
from functools import wraps
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render, resolve_url
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from sc4py.datetime import now
from solicitacao.models import Chamada


def selecionado_passes_test(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request, 'selecionado') and test_func(request.selecionado):
                if request.method == 'POST' and hasattr(request.selecionado, 'solicitacao') and request.selecionado.solicitacao.apenas_leitura:
                    return redirect("solicitacao:formulario", chamada_id=request.selecionado.chamada.id)
                if "chamada_id" in kwargs:
                    chamada_id = kwargs["chamada_id"]
                    if request.selecionado.chamada.id != chamada_id:
                        return HttpResponseForbidden("Você não tem permissão nesta solicitação de matrícula.", content_type='text/html; charset=utf-8')
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            return redirect(resolve_url("solicitacao:auth_entrar", kwargs.get("chamada_id", None)))
        return _wrapped_view
    return decorator

def public_login_required(function=None):
    actual_decorator = selecionado_passes_test(lambda u: u is not None and u.is_authenticated)
    if function:
        return actual_decorator(function)
    return actual_decorator
