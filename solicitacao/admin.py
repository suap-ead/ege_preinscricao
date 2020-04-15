from django.contrib.admin import register, ModelAdmin, TabularInline
from import_export.admin import ImportExportModelAdmin
from .models import Documentacao, Edital, DocumentoExigido, Chamada, Selecionado, Solicitacao


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
    inlines = [SelecionadoInline]
