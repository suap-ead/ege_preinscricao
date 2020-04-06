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
from django.contrib.auth.middleware import AuthenticationMiddleware
from sc4py.datetime import now
from .models import Chamada, PublicAuthToken, Solicitacao
from .forms import SolicitacaoForm, SelecionadoForm, EntrarForm
from .decorators import public_login_required


def index(request):
    default_order = ["inicio_solicitacoes", "id"]
    chamadas_em_aberto = Chamada.objects.filter(inicio_solicitacoes__lte=now(), fim_solicitacoes__gte=now()).order_by(*default_order)
    futuras_chamadas = Chamada.objects.filter(inicio_solicitacoes__gte=now()).order_by(*default_order)
    chamadas_passadas = Chamada.objects.filter(fim_solicitacoes__lte=now()).order_by(*default_order)
    return render(request, template_name='pre_matricula/index.html', context=locals())


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
    try:
        del request.session['selecionado_id']
    except KeyError:
        pass
    return redirect('solicitacao:index')


@public_login_required
def solicitacao(request, chamada_id):
    solicitacao=getattr(request.selecionado, 'solicitacao', None)
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, instance=solicitacao)
        if form.is_valid():
            form.instance.selecionado = request.selecionado
            form.save()
            form.messages = [
                "Solicitação salva com sucesso."
            ]
    else:
        form = SolicitacaoForm(instance=solicitacao)

    return render(
        request, 
        'pre_matricula/solicitacao.html', 
        {
            'form': form, 
            'chamada': request.selecionado.chamada, 
            "selecionado": request.selecionado
        }
    )
