from django.db.models import Model, CharField, DateField, BooleanField, ForeignKey
from pre_cadastro.models.nacionalidade import Nacionalidade
from pre_cadastro.models.sexo import Sexo
from pre_cadastro.models.estado_civil import EstadoCivil
from pre_cadastro.models.parentesco_responsavel import ParentescoResponsavel
from pre_cadastro.models.cidade import Cidade
from pre_cadastro.models.tipo_zona_residencial import TipoZonaResidencial
from pre_cadastro.models.tipo_necessidade_especial import TipoNecessidadeEspecial
from pre_cadastro.models.transtorno import Transtorno
from pre_cadastro.models.superdotacao import Superdotacao
from pre_cadastro.models.utiliza_transporte_escolar_publico import UtilizaTransporteEscolarPublico
from pre_cadastro.models.poder_publico_responsavel_transporte import PoderPublicoResponsavelTransporte
from pre_cadastro.models.tipo_veiculo import TipoVeiculo


class Solicitacao(Model):

  # Dados da solicitação de matrícula
  ano_letivo = ForeignKey(cartorio, verbose="Ano letivo")
  periodo_letivo = ForeignKey(cartorio, verbose="Período letivo")
  turno = ForeignKey(cartorio, verbose="Turno")
  forma_ingresso = ForeignKey(cartorio, verbose="Forma de ingresso")
  polo = ForeignKey(cartorio, verbose="Polo EAD", null=True, blank=True)
  cota_sistec = ForeignKey(cartorio, verbose="Cota SISTEC", null=True, blank=True)
  cota_mec = ForeignKey(cartorio, verbose="Cota MEC", null=True, blank=True)
  convenio = ForeignKey(cartorio, verbose="Convênio", null=True, blank=True)
  data_conclusao_intercambio = DateField("Conclusão do intercâmbio", null=True, blank=True)
  matriz_curso = ForeignKey(cartorio, verbose="Matriz/Curso")
  linha_pesquisa = ForeignKey(cartorio, verbose="Linha de pesquisa", help_text='Obrigatório para alunos de Mestrado e Doutourado. Caso não saiba, escreva "A definir".')
  aluno_especial = ForeignKey(cartorio, verbose="Aluno especial?", help_text='Marque essa opção caso se trate de um aluno especial em curso de pós-graduação')
  numero_pasta = ForeignKey(cartorio, verbose="Número da pasta")

  # Identificação
  nacionalidade = ForeignKey(Nacionalidade, verbose="Nacionalidade")
  cpf = CharField("CPF", max_length=11, null=True, blank=True)
  passaporte = CharField("Passaporte", max_length=250, null=True, blank=True)

  # Dados pessoais 
  nome = CharField("Nome", max_length=250)
  nome_social = CharField("Nome social", max_length=250, null=True, blank=False, help_text="Só preencher este campo a pedido do aluno e de acordo com a legislação vigente.")
  sexo = ForeignKey(Sexo, verbose="Sexo")
  data_nascimento = DateField("Data de nascimento")
  estado_civil = ForeignKey(EstadoCivil, verbose="Estado civil")

  # Dados familiares
  nome_pai = CharField("Nome do pai", max_length=250, null=True, blank=True)
  estado_civil_pai = ForeignKey(EstadoCivil, verbose="Estado civil do pai", null=True, blank=True)
  pai_falecido = BooleanField("Pai é falecido?", null=True, blank=True)
  nome_mae = CharField("Nome da mãe", max_length=250)
  estado_civil_mae = ForeignKey(EstadoCivil, verbose="Estado civil da mãe")
  mae_falecida = BooleanField("Mãe é falecida?")
  responsavel = CharField("Nome do responsável", max_length=250, null=True, blank=True, help_text="Obrigatório para menores de idade.")
  email_responsavel = CharField("Email do responsável", max_length=250, null=True, blank=True)
  parentesco_responsavel = ForeignKey(ParentescoResponsavel, verbose="Parentesco do responsável")
  cpf_responsavel = CharField("CPF do responsável", max_length=11, null=True, blank=True)
  
  # Endereço
  cep = CharField("CEP", max_length=9, null=True, blank=True, help_text='Formato: "99999-999"')
  logradouro = CharField("Logradouro", max_length=250)
  numero = CharField("Número", max_length=250)
  complemento = CharField("Complemento", max_length=250)
  bairro = CharField("Bairro", max_length=250)
  cidade = ForeignKey(Cidade, verbose="Cidade")
  estado = CharField("Estado", max_length=250)
  tipo_zona_residencial = ForeignKey(Cidade, verbose="Zona residencial")

  # Informações para Contato
  telefone_principal = CharField("Telefone principal", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
  telefone_secundario = CharField("Telefone secundário", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
  telefone_adicional_1 = CharField("Telefone principal do responsável", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
  telefone_adicional_2 = CharField("Telefone secundário do responsável", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
  email_pessoal = CharField("E-mail pessoal", max_length=255, null=True, blank=True, help_text='É por este email que você configurará sua senha e acompanhará suas aulas. Informe um que costume acessar.')

  # Deficiências, transtornos e superdotação
  aluno_pne = BooleanField("Portador de necessidades especiais")
  tipo_necessidade_especial = ForeignKey(TipoNecessidadeEspecial, verbose="Deficiência")
  tipo_transtorno = ForeignKey(Transtorno, verbose="Transtorno")
  superdotacao = ForeignKey(Superdotacao, verbose="Superdotação")

  # Transporte rscolar utilizado
  utiliza_transporte_escolar_publico = ForeignKey(UtilizaTransporteEscolarPublico, verbose="Utiliza transporte escolar público", null=True, blank=True)
  poder_publico_responsavel_transporte = ForeignKey(PoderPublicoResponsavelTransporte, verbose="Poder público responsável pelo transporte escolar", null=True, blank=True)
  tipo_veiculo = ForeignKey(TipoVeiculo, verbose="Tipo de veículo utilizado no transporte escolar", null=True, blank=True)

  # Outras informações
  tipo_sanguineo = ForeignKey(TipoSanguineo, verbose="Tipo sanguíneo", null=True, blank=True)
  pais_origem = ForeignKey(PaisOrigem, verbose="País de origem", null=True, blank=True, help_text="Obrigatório para estrangeiros")
  estado_naturalidade = ForeignKey(TipoVeiculo, verbose="Tipo de veículo utilizado no transporte escolar", null=True, blank=True)
  naturalidade = ForeignKey(Cidade, verbose="Naturalidade", null=True, blank=True)
  raca = ForeignKey(Cidade, verbose="Raça")

  # Dados escolares anteriores
  nivel_ensino_anterior = ForeignKey(NivelEnsino, verbose="Nível de ensino")
  tipo_instituicao_origem = ForeignKey(TipoInstituicaoOrigem, verbose="Tipo da instituição")
  ano_conclusao_estudo_anterior = ForeignKey(Ano, verbose="Ano de conclusão")

  # RG
  numero_rg = CharField("Número do RG", max_length=255, null=True, blank=True)
  uf_emissao_rg = ForeignKey(UF, verbose="Estado emissor", null=True, blank=True)
  orgao_emissao_rg = ForeignKey(orgao_emissao_rg, verbose="Orgão emissor", null=True, blank=True)
  data_emissao_rg = DateField("Data de emissão", null=True, blank=True)

  # Título de eleitor
  numero_titulo_eleitor = CharField("Título de eleitor", max_length=255, null=True, blank=True)
  zona_titulo_eleitor = ForeignKey(UF, verbose="Zona", null=True, blank=True)
  secao = ForeignKey(orgao_emissao_rg, verbose="Seção", null=True, blank=True)
  data_emissao_titulo_eleitor = DateField("Data de emissão", null=True, blank=True)
  uf_emissao_titulo_eleitor = ForeignKey(orgao_emissao_rg, verbose="Estado emissor", null=True, blank=True)

  # Carteira de reservista
  numero_carteira_reservista = CharField("Número da carteira de reservista", max_length=255, null=True, blank=True)
  regiao_carteira_reservista = CharField("Região", max_length=255, null=True, blank=True)
  serie_carteira_reservista = CharField("Série", max_length=255, null=True, blank=True)
  estado_emissao_carteira_reservista = estado_emissao_carteira_reservista(estado_emissao_carteira_reservista, verbose="Estado emissor", null=True, blank=True)
  nivel_ensino_anterior = ForeignKey(NivelEnsino, verbose="Nível de ensino", null=True, blank=True)
  ano_carteira_reservista = CharField("Ano", max_length=255, null=True, blank=True)

  # Certidão Civil
  tipo_certidao = ForeignKey(tipo_certidao, verbose="Tipo de certidão")
  cartorio = ForeignKey(cartorio, verbose="Cartório", null=True, blank=True)
  numero_certidao = CharField("Número de Termo", max_length=255, null=True, blank=True)
  folha_certidao = CharField("Folha", max_length=255, null=True, blank=True)
  livro_certidao = CharField("Livro", max_length=255, null=True, blank=True)
  data_emissao_certidao = DateField("Data de emissão", null=True, blank=True)
  matricula_certidao = CharField("Livro", max_length=255, null=True, blank=True, help_text="Obrigatório para certidões realizadas a partir de 01/01/2010")

  # Foto
  arquivo_foto = CharField("Foto", max_length=255, null=True, blank=True, help_text="Obrigatório para certidões realizadas a partir de 01/01/2010")

  # Carteira estudantil
  autorizacao_carteira_estudantil = BooleanField("Autorização para emissão da carteira estudantil", help_text="O aluno autoriza o envio de seus dados pessoais para o Sistema Brasileiro de Educação (SEB) para fins de emissão da carteira de estudante digital de acordo com a Medida Provisória Nº 895, de 6 de setembro de 2019")


  def __str__(self):
    return self.cpf