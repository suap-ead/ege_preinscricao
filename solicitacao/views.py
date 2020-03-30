import json
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from sc4py.datetime import now
from solicitacao.models import Chamada


def index(request):
    chamadas_em_aberto = Chamada.objects.filter(inicio_solicitacoes__lte=now(), fim_solicitacoes__gte=now())
    futuras_chamadas = Chamada.objects.filter(inicio_solicitacoes__gte=now())
    chamadas_passadas = Chamada.objects.filter(fim_solicitacoes__lte=now())
    return render(request, template_name='pre_matricula/index.html', context=locals())
