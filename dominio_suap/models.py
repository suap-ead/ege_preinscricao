from django.db import models


class BaseModel(models.Model):
  suap_id = models.CharField(max_length=255, unique=True)
  titulo = models.CharField(max_length=255)

  class Meta:
    abstract = True
 
  def __str__(self):
    return self.titulo


class AnoConclusao(BaseModel):
  class Meta:
    verbose_name = "Ano de conclusão"
    verbose_name_plural = "Anos de conclusão"
    ordering = ['titulo']


class AnoLetivo(BaseModel):
  class Meta:
    verbose_name = "Ano letivo"
    verbose_name_plural = "Anos letivos"
    ordering = ['titulo']


class Convenio(BaseModel):
  class Meta:
    verbose_name = "Convênio"
    verbose_name_plural = "Convênios"
    ordering = ['titulo']


class OrgaoEmissorRG(BaseModel):
  class Meta:
    verbose_name = "Órgão emissor de RG"
    verbose_name_plural = "Órgãos emissores de RG"
    ordering = ['titulo']


class ZonaResidencial(BaseModel):
  class Meta:
    verbose_name = "Zona residêncial"
    verbose_name_plural = "Zonas residênciais"
    ordering = ['titulo']


class Turno(BaseModel):
  class Meta:
    verbose_name = "Turno"
    verbose_name_plural = "Turnos"
    ordering = ['titulo']


class TransportePublico(BaseModel):
  class Meta:
    verbose_name = "Transporte público"
    verbose_name_plural = "Transportes públicos"
    ordering = ['titulo']


class TipoVeiculo(BaseModel):
  class Meta:
    verbose_name = "Tipo de veículo"
    verbose_name_plural = "Tipos de veículos"
    ordering = ['titulo']


class TipoTranstorno(BaseModel):
  class Meta:
    verbose_name = "Tipo de transtorno"
    verbose_name_plural = "Tipos de transtornos"
    ordering = ['titulo']


class TipoNecessidadeEspecial(BaseModel):
  class Meta:
    verbose_name = "Necessidade especial"
    verbose_name_plural = "Necessidades especiais"
    ordering = ['titulo']


class TipoTransporte(BaseModel):
  class Meta:
    verbose_name = "Tipo de transporte"
    verbose_name_plural = "Tipos de transporte"
    ordering = ['titulo']


class TipoSanguineo(BaseModel):
  class Meta:
    verbose_name = "Tipo sanguíneo"
    verbose_name_plural = "Tipos sanguíneos"
    ordering = ['titulo']


class TipoInstituicao(BaseModel):
  class Meta:
    verbose_name = "Tipo de instituição"
    verbose_name_plural = "Tipos de instituições"
    ordering = ['titulo']


class TipoCertidao(BaseModel):
  class Meta:
    verbose_name = "Tipo de certidão"
    verbose_name_plural = "Tipos de certidões"
    ordering = ['titulo']


class TipoSuperdotacao(BaseModel):
  class Meta:
    verbose_name = "Supordotação"
    verbose_name_plural = "Supordotações"
    ordering = ['titulo']


class Sexo(BaseModel):
  class Meta:
    verbose_name = "Sexo"
    verbose_name_plural = "Sexos"
    ordering = ['titulo']


class Responsavel(BaseModel):
  class Meta:
    verbose_name = "Responsável"
    verbose_name_plural = "Responsáveis"
    ordering = ['titulo']


class Raca(BaseModel):
  class Meta:
    verbose_name = "Raça"
    verbose_name_plural = "Raças"
    ordering = ['titulo']


class Polo(BaseModel):
  class Meta:
    verbose_name = "Pólo"
    verbose_name_plural = "Pólos"
    ordering = ['titulo']


class PeriodoLetivo(BaseModel):
  class Meta:
    verbose_name = "Período letivo"
    verbose_name_plural = "Períodos letivos"
    ordering = ['titulo']


class PaisOrigem(BaseModel):
  class Meta:
    verbose_name = "País de origem"
    verbose_name_plural = "Países de origem"
    ordering = ['titulo']


class NivelEnsino(BaseModel):
  class Meta:
    verbose_name = "Nível de ensino"
    verbose_name_plural = "Níveis de ensino"
    ordering = ['titulo']


class Nacionalidade(BaseModel):
  class Meta:
    verbose_name = "Nacionalidade"
    verbose_name_plural = "Nacionalidades"
    ordering = ['titulo']


class FormaIngresso(BaseModel):
  class Meta:
    verbose_name = "Forma de ingresso"
    verbose_name_plural = "Formas de ingressos"
    ordering = ['titulo']


class Estado(BaseModel):
  class Meta:
    verbose_name = "Estado"
    verbose_name_plural = "Estados"
    ordering = ['titulo']


class Cidade(BaseModel):
  estado = FK("Estado", Estado)
  class Meta:
    verbose_name = "Cidade"
    verbose_name_plural = "Cidades"
    ordering = ['titulo']


class EstadoCivil(BaseModel):
  class Meta:
    verbose_name = "Estado civil"
    verbose_name_plural = "Estados civis"
    ordering = ['titulo']


class CotaSISTEC(BaseModel):
  class Meta:
    verbose_name = "Cota SISTEC"
    verbose_name_plural = "Cotas SISTEC"
    ordering = ['titulo']


class CotaMEC(BaseModel):
  class Meta:
    verbose_name = "Cota MEC"
    verbose_name_plural = "Cotas MEC"
    ordering = ['titulo']


class MatrizCurso(BaseModel):
  class Meta:
    verbose_name = "Matriz/Curso"
    verbose_name_plural = "Matrizes/Cursos"
    ordering = ['titulo']


class LinhaPesquisa(BaseModel):
  class Meta:
    verbose_name = "Linha de pesquisa"
    verbose_name_plural = "Linhas de pesquisas"
    ordering = ['titulo']
