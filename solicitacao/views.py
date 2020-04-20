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
from .models import Chamada, PublicAuthToken, Solicitacao, DocumentoExigido, Documento, ListaSelecao
from .forms import EntrarForm, SolicitacaoForm, ConclusaoForm, DocumentoForm
from .decorators import public_login_required
from django.utils.timezone import now, timedelta



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


def auth_autenticar(request, token):
    pat = PublicAuthToken.objects.filter(token=token).select_related('selecionado').first()
    if pat is None:
        return render(request, 'pre_matricula/acesso/token_nao_encontrado.html')
        
    selecionado = pat.selecionado
    if pat.criado_em < now() - timedelta(hours=2):
        return render(request, 'pre_matricula/acesso/token_expirado.html', locals())
    request.session['selecionado_id'] = selecionado.id
    PublicAuthToken.objects.filter(criado_em__lt=now() - timedelta(hours=2)).delete()
    pat.delete()
    return redirect("solicitacao:formulario", chamada_id=selecionado.chamada_id)


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
    selecionado = request.selecionado
    chamada = selecionado.chamada
    solicitacao = getattr(request.selecionado, 'solicitacao', None)
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, instance=solicitacao)
        if form.is_valid():
            form.instance.selecionado = selecionado
            form.save()
            form.messages = ["Solicitação salva com sucesso."]
    else:
        form = SolicitacaoForm(instance=solicitacao)
    active_tab = "form"

    result = render(request, 'pre_matricula/solicitacao/formulario.html', context=locals())
    return result 


@public_login_required
def solicitacao_anexar(request, chamada_id=None):
    selecionado = request.selecionado
    solicitacao = request.selecionado.solicitacao
    if request.method == 'POST' and request.FILES['arquivo']:
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.messages = ["Arquivo armazenado com sucesso."]
            form = DocumentoForm(initial={'solicitacao': solicitacao})
    else:
        form = DocumentoForm(initial={'solicitacao': solicitacao})
    documentos = Documento.objects.filter(solicitacao_id=solicitacao.id)
    documentosExigidos = DocumentoExigido.objects.filter(
        edital_id=selecionado.chamada.edital.id,
        lista__in=[ListaSelecao.GERAL, selecionado.lista]
    ).exclude(
        documentacao_id__in=[x.documentacao.id for x in documentos.all()],
    )
    active_tab = "file"
    return render(request, template_name='pre_matricula/solicitacao/anexar.html', context=locals())


@public_login_required
def solicitacao_concluir(request, chamada_id):
    selecionado = request.selecionado
    if selecionado.chamada.id != chamada_id:
        raise Exception("Você não tem permissão para aceitar os termos desta solicitação de matrícula.")

    if not selecionado.solicitacao.pode_aceitar:
        raise Exception("Você não tem permissão para aceitar os termos desta solicitação de matrícula. Motivo: você ainda não aceitou enviou todos os arquivos.")

    if request.method == 'POST':
        form = ConclusaoForm(request.POST, instance=selecionado.solicitacao)
        if form.is_valid():
            form.save()
            form.messages = ["Solicitação concluída com sucesso."]
            return redirect("solicitacao:formulario", chamada_id=selecionado.chamada.id)

    form = ConclusaoForm(instance=selecionado.solicitacao)
    active_tab = "send"
    return render(request, template_name='pre_matricula/solicitacao/concluir.html', context=locals())


@public_login_required
def documento_remover(request, documento_id):
    doc = Documento.objects.get(id=documento_id)
    if request.selecionado.solicitacao.id != doc.solicitacao.id:
        raise Exception("Você não tem permissão para excluir este arquivo")
    if hasattr(request.selecionado, 'solicitacao') and request.selecionado.solicitacao.apenas_leitura:
        return redirect("solicitacao:anexar", chamada_id=request.selecionado.chamada.id)
    doc.delete()
    return redirect("solicitacao:anexar", chamada_id=request.selecionado.chamada.id)
