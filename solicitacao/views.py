import json
from django.conf import settings
from django.conf.urls.static import static
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
from .models import Chamada, PublicAuthToken, Solicitacao, DocumentoExigido, Documento, SolicitacaoConcluida
from .forms import SolicitacaoForm, SelecionadoForm, EntrarForm, DocumentoForm, SolicitacaoConcluidaForm
from .decorators import public_login_required


def auth_entrar(request, chamada_id=None):
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


def auth_autenticar(request, chamada_id, inscricao, token):
    publicAuthToken = get_object_or_404(PublicAuthToken, chamada_id=chamada_id, selecionado__inscricao=inscricao, token=token)
    publicAuthToken.delete()
    request.session['selecionado_id'] = publicAuthToken.selecionado.id
    return redirect("solicitacao:formulario", chamada_id=chamada_id)


def auth_sair(request):
    try:
        del request.session['selecionado_id']
    except KeyError:
        pass
    return redirect('solicitacao:index')


def solicitacao_index(request):
    default_order = ["inicio_solicitacoes", "id"]
    chamadas_em_aberto = Chamada.objects.filter(inicio_solicitacoes__lte=now(), fim_solicitacoes__gte=now()).order_by(*default_order)
    futuras_chamadas = Chamada.objects.filter(inicio_solicitacoes__gte=now()).order_by(*default_order)
    chamadas_passadas = Chamada.objects.filter(fim_solicitacoes__lte=now()).order_by(*default_order)
    return render(request, template_name='pre_matricula/solicitacao/index.html', context=locals())


@public_login_required
def solicitacao_formulario(request, chamada_id):
    solicitacao=getattr(request.selecionado, 'solicitacao', None)
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, instance=solicitacao)
        if form.is_valid():
            form.instance.selecionado = request.selecionado
            form.save()
            form.messages = ["Solicitação salva com sucesso."]
    else:
        form = SolicitacaoForm(instance=solicitacao)

    params = {
        "form": form,
        "selecionado": request.selecionado,
        "chamada": request.selecionado.chamada,
        # "documentosExigidos": DocumentoExigido.objects.filter(edital_id=request.selecionado.chamada.edital),
    }
    # if solicitacao is not None:
    #     params["solicitacao"] = solicitacao
    #     params["documentoForm"] = DocumentoForm(initial={'solicitacao': solicitacao.id})
    #     params["documentos"] = Documento.objects.filter(solicitacao_id=solicitacao.id)
    #     if SolicitacaoConcluida.objects.filter(solicitacao_id=solicitacao.id).first() is not None:
    #         params["solicitacaoConcluidaForm"] = SolicitacaoConcluidaForm(instance=solicitacao.solicitacaoconcluida)
    #     else:
    #         params["solicitacaoConcluidaForm"] = SolicitacaoConcluidaForm(initial={'solicitacao': solicitacao.id})

    return render(request, 'pre_matricula/solicitacao/formulario.html', params)


@public_login_required
def solicitacao_anexar(request, chamada_id=None):
    selecionado = request.selecionado
    solicitacao = request.selecionado.solicitacao
    if request.method == 'POST' and request.FILES['arquivo']:
        documentoForm = DocumentoForm(request.POST, request.FILES)
        if documentoForm.is_valid():
            documentoForm.save()
            documentoForm.messages = ["Arquivo armazenado com sucesso."]
    else:
        documentoForm = DocumentoForm(initial={'solicitacao': solicitacao})
    documentos = Documento.objects.filter(solicitacao_id=solicitacao.id)
    print(render(request, template_name='pre_matricula/solicitacao/anexar.html', context=locals()))
    return render(request, template_name='pre_matricula/solicitacao/anexar.html', context=locals())


@public_login_required
def solicitacao_concluir(request):
    if request.method == 'POST':
        form = SolicitacaoConcluidaForm(request.POST)
        if form.is_valid():
            form.save()
            form.messages = ["Inscrição efetuada com sucesso."]
    return HttpResponseRedirect("/pre_matricula/%s/solicitacao#concluir?dados_invalidos=True" % (request.POST['solicitacao']))


@public_login_required
def documento_remover(request, documento_id):
    doc = Documento.objects.get(id = documento_id)
    solicitacao_id = doc.solicitacao.id
    doc.delete()
    return HttpResponseRedirect("/pre_matricula/%s/solicitacao#file" % (solicitacao_id))
