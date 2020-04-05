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
from .forms import SolicitacaoForm, SelecionadoForm


def index(request):
    chamadas_em_aberto = Chamada.objects.filter(inicio_solicitacoes__lte=now(), fim_solicitacoes__gte=now())
    futuras_chamadas = Chamada.objects.filter(inicio_solicitacoes__gte=now())
    chamadas_passadas = Chamada.objects.filter(fim_solicitacoes__lte=now())
    return render(request, template_name='pre_matricula/index.html', context=locals())

def solicitacao(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SolicitacaoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SolicitacaoForm()

    return render(request, 'pre_matricula/solicitacao.html', {'form': form})

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
