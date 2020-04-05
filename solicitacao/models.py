from django.db.models import Model, TextChoices
from django.db.models import CharField, DateField, BooleanField, NullBooleanField, DateTimeField
from django.db.models import URLField, EmailField, FileField
# from django.db.models import ImageField
from django.contrib.auth.models import User
from django.db.models import ForeignKey, CASCADE
from dominio_suap.models import *
from .fields import nullable, nullable_phone, FK, NullFK


class Documentacao(Model):
    identificacao = CharField("Identificação", max_length=255)

    class Meta:
        verbose_name = "Documentação"
        verbose_name_plural = "Documentações"

    def __str__(self):
        return self.identificacao


class Edital(Model):
    identificacao = CharField("Identificação", max_length=255)
    titulo = CharField("Título", max_length=255)
    pagina = URLField("Página")
    tem_ppi = BooleanField("Tem lista PPI?")
    tem_pce = BooleanField("Tem lista PCD?")

    class Meta:
        verbose_name = "Edital"
        verbose_name_plural = "Editais"

    def __str__(self):
        return self.identificacao


class DocumentoExigido(Model):
    edital = FK("Edital", Edital)
    documentacao = FK("Documentação", Documentacao)
    lista_geral = BooleanField("Exigir na lista geral?")
    lista_ppi = BooleanField("Exigir na lista PPI?")
    lista_pce = BooleanField("Exigir na lista PCD?")

    class Meta:
        verbose_name = "Documento exigido"
        verbose_name_plural = "Documentos exigidos"

    def __str__(self):
        tem = []

        if self.lista_geral:
            tem.append("Geral")

        if self.lista_ppi:
            tem.append("PPI")

        if self.lista_pce:
            tem.append("PDE")

        tem_str = ""
        if len(tem):
            tem_str = " (%s)" % (tem, )

        return "%s - %s%s" % (self.edital, self.documentacao, tem_str)


class TipoChamada(TextChoices):
    INICIAL = 'I', 'Inicial'
    REMANESCENTE = 'R', 'Remanescente'


class Chamada(Model):
    edital = FK("Edital", Edital)
    chamada = CharField("Chamada", max_length=255)
    tipo_chamada = CharField("Tipo", max_length=1, choices=TipoChamada.choices, default=TipoChamada.INICIAL)
    inicio_solicitacoes = DateTimeField("Início das solicitações")
    fim_solicitacoes = DateTimeField("Fim das solicitações")

    class Meta:
        verbose_name = "Chamada"
        verbose_name_plural = "Chamadas"

    def __str__(self):
        return "%s - %s" % (self.edital, self.chamada)


class ListaSelecao(TextChoices):
    GERAL = 'GERAL', 'Geral'
    PPI = 'PPI', 'Preto/Pardo/Indígena'
    PCD = 'PCD', 'Pessoa com deficiência'


class Selecionado(Model):

    # Dados do edital
    chamada = FK("Edital", Chamada)

    # Dados da oferta
    matriz_curso = FK("Matriz/Curso", MatrizCurso, )
    ano_letivo = FK("Ano letivo", AnoLetivo)
    periodo_letivo = FK("Período letivo", PeriodoLetivo)
    turno = FK("Turno", Turno)
    forma_ingresso = FK("Forma de ingresso", FormaIngresso)
    polo = NullFK("Polo EAD", Polo)

    # Dados do selecionado
    lista = CharField("Lista de seleção", max_length=250, choices=ListaSelecao.choices)
    nacionalidade = FK("Nacionalidade", Nacionalidade)
    cpf = CharField("CPF", max_length=11, **nullable)
    passaporte = CharField("Passaporte", max_length=250, **nullable)
    nome = CharField("Nome", max_length=250)
    nome_social = CharField("Nome social", max_length=250, help_text="Só preencher este campo a pedido do aluno e de acordo com a legislação vigente.", **nullable)
    email = EmailField("E-Mail")
    inscricao = CharField("Inscrição", max_length=250, **nullable)

    class Meta:
        verbose_name = "Documentação"
        verbose_name_plural = "Documentações"

    def __str__(self):
        ident = ""
        if self.cpf:
            ident = self.cpf
        else:
            ident = self.passaporte

        return "%s - %s" % (ident, self.edital)


class Solicitacao(Model):

    # Dados da solicitação de matrícula
    selecionado = FK("Selecionado", Selecionado)
    cota_sistec = NullFK("Cota SISTEC", CotaSISTEC)
    cota_mec = NullFK("Cota MEC", CotaMEC, )
    convenio = NullFK("Convênio", Convenio, )
    data_conclusao_intercambio = DateField("Conclusão do intercâmbio", **nullable)
    linha_pesquisa = FK("Linha de pesquisa", LinhaPesquisa, help_text='Obrigatório para alunos de Mestrado e Doutourado. Caso não saiba, escreva "A definir".')
    aluno_especial = NullBooleanField("Aluno especial?")
    # numero_pasta = CharField("Número da pasta", max_length=250, null=True, blank=False)

    # Identificação
    nacionalidade = FK("Nacionalidade", Nacionalidade)
    cpf = CharField("CPF", max_length=11, **nullable)
    passaporte = CharField("Passaporte", max_length=250, **nullable)

    # Dados pessoais 
    nome = CharField("Nome", max_length=250)
    nome_social = CharField("Nome social", max_length=250, help_text="Só preencher este campo a pedido do aluno e de acordo com a legislação vigente.", **nullable)
    sexo = FK("Sexo", Sexo)
    data_nascimento = DateField("Data de nascimento")
    estado_civil = FK("Estado civil", EstadoCivil, related_name="solicitacoes")

    # Dados familiares
    nome_pai = CharField("Nome do pai", max_length=250, **nullable)
    estado_civil_pai = NullFK("Estado civil do pai", EstadoCivil, related_name="pais")
    pai_falecido = NullBooleanField("Pai é falecido?")
    nome_mae = CharField("Nome da mãe", max_length=250)
    estado_civil_mae = FK("Estado civil da mãe", EstadoCivil, related_name="maes")
    mae_falecida = BooleanField("Mãe é falecida?")
    responsavel = CharField("Nome do responsável", max_length=250, help_text="Obrigatório para menores de idade.", **nullable)
    email_responsavel = EmailField("Email do responsável", max_length=250, **nullable)
    parentesco_responsavel = FK("Parentesco do responsável", Responsavel)
    cpf_responsavel = CharField("CPF do responsável", max_length=11, **nullable)

    # Endereço
    cep = CharField("CEP", max_length=9, help_text='Formato: "99999-999"', **nullable)
    logradouro = CharField("Logradouro", max_length=250)
    numero = CharField("Número", max_length=250)
    complemento = CharField("Complemento", max_length=250)
    bairro = CharField("Bairro", max_length=250)
    cidade = FK("Cidade", Cidade, related_name="enderecos")
    estado = CharField("Estado", max_length=250)
    tipo_zona_residencial = FK("Zona residencial", ZonaResidencial)

    # Informações para Contato
    telefone_principal = CharField("Telefone principal", **nullable_phone)
    telefone_secundario = CharField("Telefone secundário", **nullable_phone)
    telefone_adicional_1 = CharField("Telefone principal do responsável", **nullable_phone)
    telefone_adicional_2 = CharField("Telefone secundário do responsável", **nullable_phone)
    email_pessoal = EmailField("E-mail pessoal", help_text='É por este email que você configurará sua senha e acompanhará suas aulas. Informe um que costume acessar.', **nullable)

    # Deficiências, transtornos e superdotação
    aluno_pne = BooleanField("Portador de necessidades especiais")
    tipo_necessidade_especial = FK("Deficiência", TipoNecessidadeEspecial)
    tipo_transtorno = FK("Transtorno", TipoTranstorno)
    superdotacao = FK("Superdotação", TipoSuperdotacao)

    # Transporte rscolar utilizado
    utiliza_transporte_escolar_publico = NullBooleanField("Utiliza transporte escolar público")
    poder_publico_responsavel_transporte = NullFK("Poder público responsável pelo transporte escolar", TipoTransporte)
    tipo_veiculo = NullFK("Tipo de veículo utilizado no transporte escolar", TipoVeiculo)

    # Outras informações
    tipo_sanguineo = NullFK("Tipo sanguíneo", TipoSanguineo)
    pais_origem = NullFK("País de origem", PaisOrigem, help_text="Obrigatório para estrangeiros")
    estado_naturalidade = NullFK("Tipo de veículo utilizado no transporte escolar", Estado, related_name="naturais")
    naturalidade = NullFK("Naturalidade", Cidade, related_name="naturalidades")
    raca = NullFK("Raça", Raca)

    # Dados escolares anteriores
    nivel_ensino_anterior = FK("Nível de ensino", NivelEnsino)
    tipo_instituicao_origem = FK("Tipo da instituição", TipoInstituicao)
    ano_conclusao_estudo_anterior = FK("Ano de conclusão", AnoConclusao)

    # RG
    numero_rg = CharField("Número do RG", max_length=255, **nullable)
    uf_emissao_rg = NullFK("Estado emissor", Estado, related_name="rgs")
    orgao_emissao_rg = NullFK("Orgão emissor", OrgaoEmissorRG)
    data_emissao_rg = DateField("Data de emissão", **nullable)

    # Título de eleitor
    numero_titulo_eleitor = CharField("Título de eleitor", max_length=255, **nullable)
    zona_titulo_eleitor = CharField("Zona", max_length=255, **nullable)
    secao = CharField("Seção", max_length=255, **nullable)
    data_emissao_titulo_eleitor = DateField("Data de emissão", **nullable)
    uf_emissao_titulo_eleitor = NullFK("Estado emissor", Estado, related_name="titulos")

    # Carteira de reservista
    numero_carteira_reservista = CharField("Número da carteira de reservista", max_length=255, **nullable)
    regiao_carteira_reservista = CharField("Região", max_length=255, **nullable)
    serie_carteira_reservista = CharField("Série", max_length=255, **nullable)
    estado_emissao_carteira_reservista = NullFK("Estado emissor", Estado, related_name="reservistas")
    nivel_ensino_anterior = NullFK("Nível de ensino", NivelEnsino)
    ano_carteira_reservista = CharField("Ano", max_length=255, **nullable)

    # Certidão Civil
    tipo_certidao = FK("Tipo de certidão", TipoCertidao)
    # cartorio = FK(Cartorio, "Cartório", **nullable)
    numero_certidao = CharField("Número de Termo", max_length=255, **nullable)
    folha_certidao = CharField("Folha", max_length=255, **nullable)
    livro_certidao = CharField("Livro", max_length=255, **nullable)
    data_emissao_certidao = DateField("Data de emissão", **nullable)
    matricula_certidao = CharField("Livro", max_length=255, help_text="Obrigatório para certidões realizadas a partir de 01/01/2010", **nullable)

    # Foto
    # arquivo_foto = ImageField("Foto", **nullable)

    # Carteira estudantil
    autorizacao_carteira_estudantil = BooleanField("Autorização para emissão da carteira estudantil", help_text="O aluno autoriza o envio de seus dados pessoais para o Sistema Brasileiro de Educação (SEB) para fins de emissão da carteira de estudante digital de acordo com a Medida Provisória Nº 895, de 6 de setembro de 2019")

    # Solicitação
    enviada_em = DateTimeField("Enviada em")
    sha512_foto = CharField("SHA 512 da foto", max_length=255)
    sha512_solicitacao = CharField("SHA 512 dos dados e arquivo", max_length=255)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"

    def __str__(self):
       return self.selecionado


class Documento(Model):
    solicitacao = FK("Solicitação", Solicitacao)
    documentacao = FK("Documentação", Documentacao)
    arquivo = FileField("Arquivo")
    sha512_arquivo = CharField("SHA 512 do arquivo", max_length=255)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
       return "%s - %s" % (self.solicitacao, self.documentacao)
