from django.db import models
from .nacionalidade import Nacionalidade
from .sexo import Sexo
from .estado_civil import EstadoCivil
from .responsavel import Responsavel
from .estado import Estado
from .zona_residencial import ZonaResidencial
from .transporte_publico import TransportePublico
from .pais_origem import PaisOrigem
from .tipo_sanguineo import TipoSanguineo
from .raca import Raca
from .nivel_ensino import NivelEnsino
from .tipo_instituicao import TipoInstituicao
from .ano_conclusao import AnoConclusao
from .necessidade_especial import NecessidadeEspecial
from .tipo_transtorno import TipoTranstorno
from .tipo_transporte import TipoTransporte
from .emissao_rg import EmissaoRg
from .tipo_certidao import TipoCertidao
from .tipo_veiculo import TipoVeiculo
from .periodo_letivo import PeriodoLetivo
from .turno import Turno
from .forma_ingresso import FormaIngresso
from .polo import Polo
from .convenio import Convenio

class Candidato(models.Model):
    nome = models.CharField(max_length=350)
    email = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    nacionalidade = models.ForeignKey(Nacionalidade, on_delete=models.CASCADE, default=None)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, default=None)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, default=None)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, default=None)
    estado = models.ForeignKey(Estado, related_name="Estado", on_delete=models.CASCADE, default=None)
    zona_residencial = models.ForeignKey(ZonaResidencial, on_delete=models.CASCADE, default=None)
    transporte_publico = models.ForeignKey(TransportePublico, on_delete=models.CASCADE, default=None)
    tipo_sanguineo = models.ForeignKey(TipoSanguineo, on_delete=models.CASCADE, default=None)
    pais_origem = models.ForeignKey(PaisOrigem, on_delete=models.CASCADE, default=None)
    estado_naturalidade = models.ForeignKey(Estado, related_name="EstadoNaturalidade", on_delete=models.CASCADE, default=None)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, default=None)
    nivel_ensino = models.ForeignKey(NivelEnsino, on_delete=models.CASCADE, default=None)
    tipo_instituicao = models.ForeignKey(TipoInstituicao, on_delete=models.CASCADE, default=None)
    ano_conclusao = models.ForeignKey(AnoConclusao, on_delete=models.CASCADE, default=None)
    necessidade_especial = models.ForeignKey(NecessidadeEspecial, on_delete=models.CASCADE, default=None)
    tipo_transtorno = models.ForeignKey(TipoTranstorno, on_delete=models.CASCADE, default=None)
    tipo_transporte = models.ForeignKey(TipoTransporte, on_delete=models.CASCADE, default=None)
    emissao_rg = models.ForeignKey(EmissaoRg, on_delete=models.CASCADE, default=None)
    tipo_certidao = models.ForeignKey(TipoCertidao, on_delete=models.CASCADE, default=None)
    periodo_letivo = models.ForeignKey(PeriodoLetivo, on_delete=models.CASCADE, default=None)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, default=None)
    forma_ingresso = models.ForeignKey(FormaIngresso, on_delete=models.CASCADE, default=None)
    polo = models.ForeignKey(Polo, on_delete=models.CASCADE, default=None)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.nome
