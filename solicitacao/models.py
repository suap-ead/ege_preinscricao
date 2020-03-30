from django.db.models import Model, CharField, DateField, BooleanField, NullBooleanField
from django.db.models import ForeignKey, CASCADE
from dominio_suap.models import *


nullable={'null':True, 'blank':True}


class FK(ForeignKey):

    def __init__(self, verbose_name, to, on_delete=CASCADE, related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=True, **kwargs):
        super().__init__(
            to, 
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            verbose_name=verbose_name,
            **kwargs)

class NullFK(ForeignKey):

    def __init__(self, verbose_name, to, on_delete=CASCADE, related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=True, **kwargs):
        if 'null' in kwargs:
            kwargs.pop('null')
        if 'blank' in kwargs:
            kwargs.pop('blank')
        super().__init__(
            to, 
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            verbose_name=verbose_name,
            null=True,
            blank=True,
            **kwargs)


class Solicitacao(Model):

    # Dados da solicitação de matrícula
    ano_letivo = FK("Ano letivo", AnoLetivo)
    periodo_letivo = FK("Período letivo", PeriodoLetivo)
    turno = FK("Turno", Turno)
    forma_ingresso = FK("Forma de ingresso", FormaIngresso)
    polo = NullFK("Polo EAD", Polo)
    cota_sistec = NullFK("Cota SISTEC", CotaSISTEC)
    cota_mec = NullFK("Cota MEC", CotaMEC, )
    convenio = NullFK("Convênio", Convenio, )
    data_conclusao_intercambio = DateField("Conclusão do intercâmbio", **nullable)
    matriz_curso = FK("Matriz/Curso", MatrizCurso, )
    linha_pesquisa = FK("Linha de pesquisa", LinhaPesquisa, help_text='Obrigatório para alunos de Mestrado e Doutourado. Caso não saiba, escreva "A definir".')
    aluno_especial = NullBooleanField("Aluno especial?")
    # numero_pasta = CharField("Número da pasta", max_length=250, null=True, blank=False)

    # Identificação
    nacionalidade = FK("Nacionalidade", Nacionalidade)
    cpf = CharField("CPF", max_length=11, null=True, blank=True)
    passaporte = CharField("Passaporte", max_length=250, null=True, blank=True)

    # Dados pessoais 
    nome = CharField("Nome", max_length=250)
    nome_social = CharField("Nome social", max_length=250, null=True, blank=False, help_text="Só preencher este campo a pedido do aluno e de acordo com a legislação vigente.")
    sexo = FK("Sexo", Sexo)
    data_nascimento = DateField("Data de nascimento")
    estado_civil = FK("Estado civil", EstadoCivil, related_name="solicitacoes")

    # Dados familiares
    nome_pai = CharField("Nome do pai", max_length=250, null=True, blank=True)
    estado_civil_pai = NullFK("Estado civil do pai", EstadoCivil, related_name="pais")
    pai_falecido = NullBooleanField("Pai é falecido?")
    nome_mae = CharField("Nome da mãe", max_length=250)
    estado_civil_mae = FK("Estado civil da mãe", EstadoCivil, related_name="maes")
    mae_falecida = BooleanField("Mãe é falecida?")
    responsavel = CharField("Nome do responsável", max_length=250, null=True, blank=True, help_text="Obrigatório para menores de idade.")
    email_responsavel = CharField("Email do responsável", max_length=250, null=True, blank=True)
    parentesco_responsavel = FK("Parentesco do responsável", Responsavel)
    cpf_responsavel = CharField("CPF do responsável", max_length=11, null=True, blank=True)

    # Endereço
    cep = CharField("CEP", max_length=9, null=True, blank=True, help_text='Formato: "99999-999"')
    logradouro = CharField("Logradouro", max_length=250)
    numero = CharField("Número", max_length=250)
    complemento = CharField("Complemento", max_length=250)
    bairro = CharField("Bairro", max_length=250)
    cidade = FK("Cidade", Cidade, related_name="enderecos")
    estado = CharField("Estado", max_length=250)
    tipo_zona_residencial = FK("Zona residencial", ZonaResidencial)

    # Informações para Contato
    telefone_principal = CharField("Telefone principal", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
    telefone_secundario = CharField("Telefone secundário", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
    telefone_adicional_1 = CharField("Telefone principal do responsável", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
    telefone_adicional_2 = CharField("Telefone secundário do responsável", max_length=15, null=True, blank=True, help_text='(XX) XXXX-XXXX')
    email_pessoal = CharField("E-mail pessoal", max_length=255, null=True, blank=True, help_text='É por este email que você configurará sua senha e acompanhará suas aulas. Informe um que costume acessar.')

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
    numero_rg = CharField("Número do RG", max_length=255, null=True, blank=True)
    uf_emissao_rg = NullFK("Estado emissor", Estado, related_name="rgs")
    orgao_emissao_rg = NullFK("Orgão emissor", OrgaoEmissorRG)
    data_emissao_rg = DateField("Data de emissão", null=True, blank=True)

    # Título de eleitor
    numero_titulo_eleitor = CharField("Título de eleitor", max_length=255, null=True, blank=True)
    zona_titulo_eleitor = CharField("Zona", max_length=255, null=True, blank=True)
    secao = CharField("Seção", max_length=255, null=True, blank=True)
    data_emissao_titulo_eleitor = DateField("Data de emissão", null=True, blank=True)
    uf_emissao_titulo_eleitor = NullFK("Estado emissor", Estado, related_name="titulos")

    # Carteira de reservista
    numero_carteira_reservista = CharField("Número da carteira de reservista", max_length=255, null=True, blank=True)
    regiao_carteira_reservista = CharField("Região", max_length=255, null=True, blank=True)
    serie_carteira_reservista = CharField("Série", max_length=255, null=True, blank=True)
    estado_emissao_carteira_reservista = NullFK("Estado emissor", Estado, related_name="reservistas")
    nivel_ensino_anterior = NullFK("Nível de ensino", NivelEnsino)
    ano_carteira_reservista = CharField("Ano", max_length=255, null=True, blank=True)

    # Certidão Civil
    tipo_certidao = FK("Tipo de certidão", TipoCertidao)
    # cartorio = FK(Cartorio, "Cartório", null=True, blank=True)
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