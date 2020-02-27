from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .modelos.nacionalidade import Nacionalidade
from .modelos.sexo import Sexo
from .modelos.estado_civil import EstadoCivil
from .modelos.responsavel import Responsavel
from .modelos.estado import Estado
from .modelos.zona_residencial import ZonaResidencial
from .modelos.transporte_publico import TransportePublico
from .modelos.tipo_sanguineo import TipoSanguineo
from .modelos.pais_origem import PaisOrigem
from .modelos.raca import Raca
from .modelos.nivel_ensino import NivelEnsino
from .modelos.tipo_instituicao import TipoInstituicao
from .modelos.candidato import Candidato

@admin.register(Nacionalidade)
@admin.register(Sexo)
@admin.register(EstadoCivil)
@admin.register(Responsavel)
@admin.register(Estado)
@admin.register(ZonaResidencial)
@admin.register(TransportePublico)
@admin.register(TipoSanguineo)
@admin.register(PaisOrigem)
@admin.register(Raca)
@admin.register(NivelEnsino)
@admin.register(TipoInstituicao)
@admin.register(Candidato)

class CandidatoAdmin(ImportExportModelAdmin):
    # list_display = ['nome', 'email', 'cpf']
    # ordering = ['nome']
    pass
