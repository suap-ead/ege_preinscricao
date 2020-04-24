import re
from django.conf import settings
from django.shortcuts import resolve_url
from django import forms
from django.forms import Form, ModelForm, ValidationError, CharField, BooleanField
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import Selecionado, Solicitacao, PublicAuthToken, Documento, ListaSelecao


class EntrarForm(Form):    
    chave = CharField(label="Informe", max_length=250, required=True)

    def __init__(self, *args, **kwargs):
        self.chamada = kwargs.pop('chamada', None)
        self.request = kwargs.pop('request', None)
        self.selecionado = None
        super().__init__(*args, **kwargs)

    def clean_chave(self):
        c = self.cleaned_data['chave']
        try:
            d = re.sub('\D', '', c)

            selecionado = self.chamada.selecionado_set.get(Q(cpf=c) | Q(cpf=d) | Q(email=c) | Q(passaporte=c) | Q(inscricao=c))
            publicAuthToken = PublicAuthToken(selecionado=selecionado)
            publicAuthToken.save()
            full_url = self.request._current_scheme_host + resolve_url("solicitacao:auth_autenticar", **{"token": publicAuthToken.token})
            try:
                send_mail(
                    'Acesso à solicitação de matrícula online do IFRN',
                    "Para terminar teu acesso, clique no link %s ."
                    " Este código só é válida por 2h e só pode ser usado uma única vez." % (full_url),
                    'ava@ifrn.edu.br',
                    [selecionado.email],
                    fail_silently=False,
                    html_message="Para terminar teu acesso, clique no link <a href='%s'>%s</a> . Esta código só é válida por 2h." % (full_url, full_url)
                )
            except Exception as e:
                raise ValidationError("Falha ao enviar email para %s" % selecionado.email)
            self.selecionado = selecionado
        except ObjectDoesNotExist as e:
            raise ValidationError("O e-mail, ou nº de inscrição, ou CPF ou passaporte não faz parte desta chamada")
        return self.cleaned_data['chave']

    def validate(self, value):
        super().validate(value)
        for email in value:
            validate_email(email)


class SolicitacaoForm(ModelForm):
    class Meta:
        model = Solicitacao
        fields = [
            'nome', 'nome_social', 'sexo', 'data_nascimento', 'estado_civil', 'nome_pai',
            'estado_civil_pai', 'pai_falecido', 'nome_mae', 'estado_civil_mae',
            'mae_falecida', 'responsavel', 'email_responsavel', 'parentesco_responsavel',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'tipo_zona_residencial', 'telefone_principal', 'telefone_secundario',
            'telefone_adicional_1', 'telefone_adicional_2', 'email_pessoal', 'aluno_pne',
            'tipo_necessidade_especial', 'tipo_transtorno', 'superdotacao',
            'utiliza_transporte_escolar_publico', 'poder_publico_responsavel_transporte',
            'tipo_veiculo', 'tipo_sanguineo', 'pais_origem', 'estado_naturalidade',
            'naturalidade', 'raca', 'nivel_ensino_anterior', 'tipo_instituicao_origem',
            'ano_conclusao_estudo_anterior', 'numero_rg', 'uf_emissao_rg',
            'orgao_emissao_rg', 'data_emissao_rg', 'numero_titulo_eleitor',
            'zona_titulo_eleitor', 'secao', 'data_emissao_titulo_eleitor',
            'uf_emissao_titulo_eleitor', 'numero_carteira_reservista',
            'regiao_carteira_reservista', 'serie_carteira_reservista',
            'estado_emissao_carteira_reservista', 'nivel_ensino_anterior',
            'ano_carteira_reservista', 'tipo_certidao', 'numero_certidao',
            'folha_certidao', 'livro_certidao', 'data_emissao_certidao',
            'matricula_certidao', 'data_conclusao_intercambio',
            'linha_pesquisa','autorizacao_carteira_estudantil']
        # widgets = {
        #     'data_conclusao_intercambio': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        #     'data_nascimento': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        #     'data_emissao_rg': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        #     'data_emissao_titulo_eleitor': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        #     'data_emissao_certidao': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        # }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields=['documentacao', 'arquivo', 'solicitacao']
        widgets = {'solicitacao': forms.HiddenInput()}


class ConclusaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['organizacao_didatica', 'autodeclaracao_etnia', 'penal', 'veracidade', 'confirmacao', ]

    def clean_organizacao_didatica(self):
        if not self.cleaned_data['organizacao_didatica']:
            raise ValidationError("Não posso concluir a solicitação se você não aceitar este termo.")
        return self.cleaned_data['organizacao_didatica']

    def clean_autodeclaracao_etnia(self):
        if self.instance.selecionado.lista == ListaSelecao.PPI:
            if not self.cleaned_data['autodeclaracao_etnia']:
                raise ValidationError("Não posso concluir a solicitação se você não aceitar este termo.")
        return self.cleaned_data['autodeclaracao_etnia']

    def clean_penal(self):
        if not self.cleaned_data['penal']:
            raise ValidationError("Não posso concluir a solicitação se você não aceitar este termo.")
        return self.cleaned_data['penal']

    def clean_veracidade(self):
        if not self.cleaned_data['veracidade']:
            raise ValidationError("Não posso concluir a solicitação se você não aceitar este termo.")
        return self.cleaned_data['veracidade']

    def clean_confirmacao(self):
        if not self.cleaned_data['confirmacao']:
            raise ValidationError("Não posso concluir a solicitação se você não aceitar este termo.")
        return self.cleaned_data['confirmacao']
