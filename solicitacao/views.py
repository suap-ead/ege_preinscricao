import json
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q
from sc4py.datetime import now
from .models import Chamada, PublicAuthToken
from .forms import SolicitacaoForm, SelecionadoForm, EntrarForm
from .decorators import public_login_required
from django.contrib.auth.middleware import AuthenticationMiddleware


def index(request):
    chamadas_em_aberto = Chamada.objects.filter(inicio_solicitacoes__lte=now(), fim_solicitacoes__gte=now())
    futuras_chamadas = Chamada.objects.filter(inicio_solicitacoes__gte=now())
    chamadas_passadas = Chamada.objects.filter(fim_solicitacoes__lte=now())
    return render(request, template_name='pre_matricula/index.html', context=locals())

@public_login_required
def solicitacao(request, chamada_id):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = SolicitacaoForm()

    return render(request, 'pre_matricula/solicitacao.html', {'form': form})

@login_required
def selecionado(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SelecionadoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SelecionadoForm()

    return render(request, 'pre_matricula/selecionado.html', {'form': form})


def entrar(request, chamada_id=None):
    if chamada_id is None:
        return redirect("solicitacao:index")

    chamada = get_object_or_404(Chamada, id=chamada_id)

    if request.method == 'POST':
        form = EntrarForm(request.POST, chamada=chamada, request=request)
        if form.is_valid():
            return render(request, 'pre_matricula/acesso/entrar.html', locals())
    else:
        form = EntrarForm()

    return render(request, 'pre_matricula/acesso/entrar.html', locals())


def autenticar(request, chamada_id, inscricao, token):
    publicAuthToken = get_object_or_404(PublicAuthToken, chamada_id=chamada_id, selecionado__inscricao=inscricao, token=token)
    publicAuthToken.delete()
    request.session['selecionado_id'] = publicAuthToken.selecionado.id
    return redirect("solicitacao:solicitacao", chamada_id=chamada_id)


def sair(request):
    return render(request, 'pre_matricula/acesso/sair.html')
