from django.contrib.admin import register, ModelAdmin, TabularInline
# from import_export.admin import ImportExportModelAdmin
from .models import Edital, Chamada, Selecionado, Solicitacao


@register(Edital)
class EditalAdmin(ModelAdmin):
    list_display = ['identificacao', 'titulo', 'pagina']
    search_fields = ['identificacao', 'titulo']

class SelecionadoInline(TabularInline):
    model = Selecionado

@register(Chamada)
class ChamadaAdmin(ModelAdmin):
    list_display = ['chamada', 'edital', 'tipo_chamada', 'inicio_solicitacoes', 'fim_solicitacoes']
    list_filter = ['tipo_chamada',  'edital__identificacao', 'chamada']
    search_fields = ['edital__identificacao', 'chamada']

    autocomplete_fields = ['edital']
    inlines = [SelecionadoInline]
