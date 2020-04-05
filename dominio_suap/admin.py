from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import register, ModelAdmin, TabularInline
from .models import *

class BaseAdmin(ModelAdmin):
    list_display = ['suap_id', 'titulo']
    search_fields = ['suap_id', 'titulo']

@register(Nacionalidade)
class NacionalidadeAdmin(BaseAdmin):
    pass

@register(Sexo)
class SexoAdmin(BaseAdmin):
    pass

@register(EstadoCivil)
class EstadoCivilAdmin(BaseAdmin):
    pass

@register(Responsavel)
class ResponsavelAdmin(BaseAdmin):
    pass

@register(Estado)
class EstadoAdmin(BaseAdmin):
    pass

@register(ZonaResidencial)
class ZonaResidencialAdmin(BaseAdmin):
    pass

@register(TransportePublico)
class TransportePublicoAdmin(BaseAdmin):
    pass

@register(TipoSanguineo)
class TipoSanguineoAdmin(BaseAdmin):
    pass

@register(PaisOrigem)
class PaisOrigemAdmin(BaseAdmin):
    pass

@register(Raca)
class RacaAdmin(BaseAdmin):
    pass

@register(NivelEnsino)
class NivelEnsinoAdmin(BaseAdmin):
    pass

@register(TipoInstituicao)
class TipoInstituicaoAdmin(BaseAdmin):
    pass

@register(AnoConclusao)
class AnoConclusaoAdmin(BaseAdmin):
    pass

@register(TipoNecessidadeEspecial)
class TipoNecessidadeEspecialAdmin(BaseAdmin):
    pass

@register(TipoTranstorno)
class TipoTranstornoAdmin(BaseAdmin):
    pass

@register(TipoSuperdotacao)
class TipoSuperdotacaoAdmin(BaseAdmin):
    pass

@register(TipoTransporte)
class TipoTransporteAdmin(BaseAdmin):
    pass

@register(TipoVeiculo)
class TipoVeiculoAdmin(BaseAdmin):
    pass

@register(TipoCertidao)
class TipoCertidaoAdmin(BaseAdmin):
    pass

@register(PeriodoLetivo)
class PeriodoLetivoAdmin(BaseAdmin):
    pass

@register(Turno)
class TurnoAdmin(BaseAdmin):
    pass

@register(FormaIngresso)
class FormaIngressoAdmin(BaseAdmin):
    pass

@register(Polo)
class PoloAdmin(BaseAdmin):
    pass

@register(Convenio)
class ConvenioAdmin(BaseAdmin):
    pass
