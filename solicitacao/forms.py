from django.conf import settings
from django import forms
from django.forms import Form, ModelForm, ValidationError, CharField
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import Selecionado, Solicitacao, PublicAuthToken, Documento

 

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
            selecionado = self.chamada.selecionado_set.get(Q(cpf=c) | Q(email=c) | Q(passaporte=c) | Q(inscricao=c))
            publicAuthToken = PublicAuthToken(chamada=self.chamada, selecionado=selecionado)
            publicAuthToken.save()
            try:
                full_url = f"{self.request._current_scheme_host}/{settings.URL_PATH_PREFIX}{self.chamada.id}/{selecionado.inscricao}/{publicAuthToken.token}/autenticar/"
                send_mail(
                    'Acesso à solicitação de matrícula online do IFRN',
                    "Para terminar teu acesso, clique no link %s. Esta código só é válida por 2h." % (full_url),
                    'ava@ifrn.edu.br',
                    [selecionado.email],
                    fail_silently=False,
                    html_message="Para terminar teu acesso, clique no link <a href='%s'>%s</a>. Esta código só é válida por 2h." % (full_url, full_url)
                )
            except Exception as e:
                print(e)
                raise ValidationError("Falha ao enviar email para %s" % selecionado.email)
            self.selecionado = selecionado
        except ObjectDoesNotExist as e:
            raise ValidationError("O e-mail, nº de inscrição, CPF ou passaporte não faz parte desta chamada")
        return self.cleaned_data['chave']

    def validate(self, value):
        super().validate(value)

        for email in value:
            validate_email(email)

class SelecionadoForm(ModelForm):

    class Meta:
        model = Selecionado
        fields = ['chamada', 'matriz_curso', 'ano_letivo', 'periodo_letivo',
            'turno', 'forma_ingresso', 'polo', 'lista', 'nacionalidade',
            'cpf', 'passaporte', 'nome', 'nome_social', 'email', 'inscricao']

class SolicitacaoForm(ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['data_conclusao_intercambio',
            'linha_pesquisa',
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
            'matricula_certidao', 'autorizacao_carteira_estudantil']
        widgets = {
            'data_conclusao_intercambio': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'data_nascimento': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'data_emissao_rg': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'data_emissao_titulo_eleitor': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'data_emissao_certidao': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields=['documentacao', 'arquivo', 'solicitacao']
        widgets = {'solicitacao': forms.HiddenInput()}
