from django.contrib.admin import register, ModelAdmin, TabularInline
from import_export.admin import ImportExportModelAdmin
from .models import Documentacao, Edital, DocumentoExigido, Chamada, Selecionado, Solicitacao, Documento


@register(Documentacao)
class DocumentacaoAdmin(ImportExportModelAdmin):
    list_display = ['identificacao']
    search_fields = ['identificacao']


class DocumentoExigidoInline(TabularInline):
    model = DocumentoExigido


@register(Edital)
class EditalAdmin(ImportExportModelAdmin):
    list_display = ['identificacao', 'titulo', 'pagina']
    search_fields = ['identificacao', 'titulo']

    inlines = [DocumentoExigidoInline]


class SelecionadoInline(TabularInline):
    model = Selecionado


@register(Chamada)
class ChamadaAdmin(ImportExportModelAdmin):
    list_display = ['chamada', 'edital', 'tipo_chamada', 'inicio_solicitacoes', 'fim_solicitacoes']
    list_filter = ['tipo_chamada',  'edital__identificacao']
    search_fields = ['edital__identificacao', 'chamada']

    autocomplete_fields = ['edital']



@register(Selecionado)
class SelecionadoAdmin(ImportExportModelAdmin):
    list_display = ['nome', 'chamada', 'cpf']
    list_filter = ['chamada__edital__identificacao', 
                   'matriz_curso__titulo']
    search_fields = ['cpf', 'email', 'inscricao', 'nome', 'nome_social', 'passaporte', 'passaporte', 'polo__titulo', ]



class DocumentoInline(TabularInline):
    model = Documento
    exclude = ['sha512_arquivo']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@register(Solicitacao)
class SolicitacaoAdmin(ImportExportModelAdmin):
    list_display = ['nome', 'selecionado']
    list_filter = ['confirmacao', 
                   'selecionado__chamada__edital__identificacao', 
                   'selecionado__matriz_curso__titulo']
    search_fields = ['selecionado__cpf', 'selecionado__email', 'selecionado__inscricao', 'selecionado__nome', 
                     'selecionado__nome_social', 'selecionado__passaporte', 'selecionado__polo__titulo', 
                     'selecionado__chamada__edital__identificacao']

    inlines = [DocumentoInline]

    readonly_fields = ['selecionado', 'data_conclusao_intercambio', 'linha_pesquisa', 
                       'nome', 'nome_social', 'sexo', 'data_nascimento', 'estado_civil', 
                       'nome_pai', 'estado_civil_pai', 'pai_falecido', 'nome_mae', 'estado_civil_mae',
                       'mae_falecida', 'responsavel', 'email_responsavel', 'parentesco_responsavel', 'cpf_responsavel', 
                       'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'tipo_zona_residencial',
                       'telefone_principal', 'telefone_secundario', 'telefone_adicional_1', 'telefone_adicional_2', 
                       'email_pessoal', 'aluno_pne', 'tipo_necessidade_especial', 'tipo_transtorno', 'superdotacao', 
                       'utiliza_transporte_escolar_publico', 'poder_publico_responsavel_transporte', 
                       'tipo_veiculo', 'tipo_sanguineo', 'pais_origem', 'estado_naturalidade', 'naturalidade', 'raca', 
                       'nivel_ensino_anterior', 
                       'tipo_instituicao_origem', 
                       'ano_conclusao_estudo_anterior', 
                       'numero_rg', 
                       'uf_emissao_rg', 
                       'orgao_emissao_rg', 
                       'data_emissao_rg', 
                       'numero_titulo_eleitor', 
                       'zona_titulo_eleitor', 
                       'secao', 
                       'data_emissao_titulo_eleitor', 
                       'uf_emissao_titulo_eleitor', 
                       'numero_carteira_reservista', 
                       'regiao_carteira_reservista', 
                       'serie_carteira_reservista', 
                       'estado_emissao_carteira_reservista', 
                       'nivel_ensino_anterior', 
                       'ano_carteira_reservista', 
                       'tipo_certidao', 
                       'numero_certidao', 
                       'folha_certidao', 
                       'livro_certidao', 
                       'data_emissao_certidao', 
                       'matricula_certidao', 
                       'autorizacao_carteira_estudantil', 
                       'organizacao_didatica', 
                       'autodeclaracao_etnia', 
                       'penal', 
                       'veracidade', 
                       'confirmacao', 
                       'enviada_em', 
                       'sha512_solicitacao', 
                       'iniciada_em', 
                       'salvo_em', 
                       ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
