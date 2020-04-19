from uuid import uuid1
import hashlib, json
from django.core import serializers
from django.core.exceptions import ValidationError
from django.utils.timezone import now
# from rest_framework import serializers
from django.db.models import Model, TextChoices
from django.db.models import CharField, DateField, BooleanField, NullBooleanField, DateTimeField, TextField
from django.db.models import URLField, EmailField, FileField, OneToOneField
from django.db.models import ImageField
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import ForeignKey, CASCADE
from dominio_suap.models import *
from .fields import nullable, nullable_phone, FK, NullFK


class ListaSelecao(TextChoices):
    GERAL = 'GERAL', 'Geral'
    PPI = 'PPI', 'Preto/Pardo/Indígena'
    PCD = 'PCD', 'Pessoa com deficiência'


class Documentacao(Model):
    identificacao = CharField("Identificação", max_length=255)

    class Meta:
        verbose_name = "Documentação"
        verbose_name_plural = "Documentações"
        ordering = ['identificacao']

    def __str__(self):
        return self.identificacao


class Edital(Model):
    identificacao = CharField("Identificação", max_length=255)
    titulo = CharField("Título", max_length=255)
    pagina = URLField("Página")

    class Meta:
        verbose_name = "Edital"
        verbose_name_plural = "Editais"
        ordering = ['identificacao', 'titulo']

    def __str__(self):
        return self.identificacao


class DocumentoExigido(Model):
    edital = FK("Edital", Edital)
    documentacao = FK("Documentação", Documentacao)
    lista = CharField("Lista de seleção", max_length=250, choices=ListaSelecao.choices)

    class Meta:
        verbose_name = "Documento exigido"
        verbose_name_plural = "Documentos exigidos"
        ordering = ['edital', 'documentacao', 'lista']

    @property
    def label_form(self):
        self.documentacao

    def __str__(self):
        return "%s - %s (%s)" % (self.edital, self.documentacao, self.lista)


class TipoChamada(TextChoices):
    INICIAL = 'I', 'Inicial'
    REMANESCENTE = 'R', 'Remanescente'


class Chamada(Model):
    edital = FK("Edital", Edital)
    chamada = CharField("Chamada", max_length=255)
    tipo_chamada = CharField("Tipo", max_length=1, choices=TipoChamada.choices, default=TipoChamada.INICIAL)
    inicio_solicitacoes = DateTimeField("Início das solicitações")
    fim_solicitacoes = DateTimeField("Fim das solicitações")
    instrucoes_adicionais = TextField("Instruções adicionais", **nullable)

    class Meta:
        verbose_name = "Chamada"
        verbose_name_plural = "Chamadas"
        ordering = ['-tipo_chamada']

    def __str__(self):
        return "%s - %s" % (self.edital, self.chamada)


class Selecionado(Model):

    # Dados do edital
    chamada = FK("Chamada", Chamada)

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

    convenio = NullFK("Convênio", Convenio, )
    cota_sistec = NullFK("Cota SISTEC", CotaSISTEC)
    cota_mec = NullFK("Cota MEC", CotaMEC, )
    aluno_especial = NullBooleanField("Aluno especial?")

    class Meta:
        verbose_name = "Selecionado"
        verbose_name_plural = "Selecionados"

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        ident = ""
        if self.cpf:
            ident = self.cpf
        else:
            ident = self.passaporte

        return "%s - %s" % (ident, self.chamada)


class PublicAuthToken(Model):
    selecionado = FK("Selecionado", Selecionado)
    token = CharField("Token", max_length=255)
    criado_em = DateTimeField("Criado em", auto_now=True)

    def save(self):
        self.token = "%s" % uuid1()
        super().save()


class Solicitacao(Model):

    # Dados da solicitação de matrícula
    selecionado = OneToOneField(Selecionado, verbose_name="Selecionado", on_delete=CASCADE)
    data_conclusao_intercambio = DateField("Conclusão do intercâmbio", **nullable)
    linha_pesquisa = NullFK("Linha de pesquisa", LinhaPesquisa, help_text='Obrigatório para alunos de Mestrado e Doutourado. Caso não saiba, escreva "A definir".')
    # numero_pasta = CharField("Número da pasta", max_length=250, null=True, blank=False)

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
    complemento = CharField("Complemento", max_length=250, **nullable)
    bairro = CharField("Bairro", max_length=250)
    cidade = FK("Cidade", Cidade, related_name="enderecos")
    estado = FK("Estado", Estado)
    tipo_zona_residencial = FK("Zona residencial", ZonaResidencial)

    # Informações para Contato
    telefone_principal = CharField("Telefone principal", **nullable_phone)
    telefone_secundario = CharField("Telefone secundário", **nullable_phone)
    telefone_adicional_1 = CharField("Telefone principal do responsável", **nullable_phone)
    telefone_adicional_2 = CharField("Telefone secundário do responsável", **nullable_phone)
    email_pessoal = EmailField("E-mail pessoal", help_text='É por este email que você configurará sua senha e acompanhará suas aulas. Informe um que costume acessar.', **nullable)

    # Deficiências, transtornos e superdotação
    aluno_pne = BooleanField("Portador de necessidades especiais")
    tipo_necessidade_especial = NullFK("Deficiência", TipoNecessidadeEspecial)
    tipo_transtorno = NullFK("Transtorno", TipoTranstorno)
    superdotacao = NullFK("Superdotação", TipoSuperdotacao)

    # Transporte rscolar utilizado
    utiliza_transporte_escolar_publico = NullBooleanField("Utiliza transporte escolar público")
    poder_publico_responsavel_transporte = NullFK("Poder público responsável pelo transporte escolar", TipoTransporte)
    tipo_veiculo = NullFK("Tipo de veículo utilizado no transporte escolar", TipoVeiculo)

    # Outras informações
    tipo_sanguineo = NullFK("Tipo sanguíneo", TipoSanguineo)
    pais_origem = NullFK("País de origem", PaisOrigem, help_text="Obrigatório para estrangeiros")
    estado_naturalidade = NullFK("Estado da naturalidade", Estado, related_name="naturais")
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
    # arquivo_foto = FileField("Foto", **nullable)
    # sha512_foto = CharField("SHA 512 da foto", max_length=255, **nullable)

    # Carteira estudantil
    autorizacao_carteira_estudantil = BooleanField("Autorização para emissão da carteira estudantil", help_text="O aluno autoriza o envio de seus dados pessoais para o Sistema Brasileiro de Educação (SEB) para fins de emissão da carteira de estudante digital de acordo com a Medida Provisória Nº 895, de 6 de setembro de 2019")

    # Termos
    organizacao_didatica = NullBooleanField("Organização didática", help_text="<p>Declaro que estou ciente das normas previstas na Organização Didática* do IFRN e que:</p>" +
        "<ol>" +
        "  <li>Terei que frequentar as aulas presenciais, independente do turno, se assim a Instituição determinar;</li>" +
        "  <li>Terei de renovar minha matrícula, periodicamente, durante o período de renovação de matrícula, previsto no Calendário Acadêmico, sob pena de ter a matrícula cancelada pela instituição;</li>" +
        "  <li>Caso deixe de frequentar as aulas (acessar o ambiente virtual), nos 10 (dez) primeiros dias úteis do início do curso, sem que seja apresentada uma justificativa, serei desligado do IFRN, sendo minha vaga preenchida por outro candidato, de acordo com a ordem classificatória do processo seletivo.</li>" +
        "  <li>O estudante não poderá ocupar matrículas simultâneas no mesmo campus ou em diferentes campi do IFRN, nas seguintes situações, independente da modalidade de ensino: em mais de um curso de pós-graduação stricto sensu, em mais de um curso de pós-graduação lato sensu; em mais de um curso de graduação; em mais de um curso técnico de nível médio. Não será permitida a matrícula simultânea em mais de dois cursos.</li>" +
        "  <li>Para os alunos de graduação, estou ciente da Lei Federal nº 12.089 de 11 de novembro de 2009, que proíbe que uma mesma pessoa ocupe 2 (duas) vagas simultaneamente em instituições públicas de ensino superior.</li>" +
        "</ol>" +
        "<p>Diante do exposto, assumo o compromisso de seguir as normas institucionais, e peço deferimento.​</p>")
    autodeclaracao_etnia = NullBooleanField("Autodeclaração de etnia", help_text="DECLARO que sou uma pessoa de cor/raça conforme meu <b>formulário de solicitação de matrícula</b>, para o fim específico de atender aos termos do <b>Edital {{chamada.edital.identificacao}} - {{chamada.edital.titulo}}</b> no que se refere à reserva de vagas da lista diferenciada com a condição de etnia.")
    penal = NullBooleanField("Declarações legais", help_text="Declaro, também, estar ciente de que, a comprovação da falsidade desta declaração, em procedimento que me assegure o contraditório e a ampla defesa, implicará no cancelamento da minha matrícula nesta Instituição Federal de Ensino, sem prejuízo das sanções penais cabíveis.")

    # Conclusão
    veracidade = NullBooleanField("Declaração de veracidade", help_text="Reconheço que as informações prestadas são verdadeiras")
    confirmacao = NullBooleanField("Declaração de conclusão", help_text="Confirmo que após concluir o meu cadastro não poderei mais alterar os dados e arquivos enviados.")
    enviada_em = DateTimeField("Enviada em", **nullable)
    sha512_solicitacao = CharField("SHA 512 dos dados e arquivo", max_length=255, **nullable)

    # Solicitação
    iniciada_em = DateTimeField("Iniciada em", auto_now_add=True)
    salvo_em = DateTimeField("Salva em", auto_now=True)

    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"

    def __str__(self):
       return "%s" % self.selecionado

    @property
    def aceitou_algum_termo(self):
        # Aceitou ao menos um dos termos?
        return  self.veracidade == True or self.confirmacao == True or self.organizacao_didatica == True or self.penal == True or self.autodeclaracao_etnia == True

    @property
    def aceitou_termos_comuns(self):
        # True se aceitou todos termos comuns, False se não aceitou algum termo comum
        return self.veracidade == True and self.confirmacao == True and self.organizacao_didatica == True and self.penal == True

    @property
    def aceitou_todos_termos(self):
        # Se foi selecionado em lista PPI, tem que aceitar a autodeclaracao_etnia
        if Selecionado.objects.get(pk=self.selecionado_id).lista == ListaSelecao.PPI:
            # Retorna True se aceitou todos e a etnia, False se não aceitou algum
            return self.aceitou_termos_comuns and self.autodeclaracao_etnia == True

        # Retorna True se aceitou todos, False se não aceitou algum
        return self.aceitou_termos_comuns

    @property
    def apenas_leitura(self):
        return self.sha512_solicitacao is not None or now() > self.selecionado.chamada.fim_solicitacoes

    @property
    def apenas_leitura_motivo(self):
        if self.sha512_solicitacao is not None:
            return "A solicitação já foi concluída por você"            

        if now() > self.selecionado.chamada.fim_solicitacoes:
            return "O período de envio já foi expirou"
        return "Ainda pode enviar"

    def cancelar_aceite(self):
        self.sha512_solicitacao = None
        self.veracidade = None
        self.confirmacao = None
        self.organizacao_didatica = None
        self.autodeclaracao_etnia = None
        self.penal = None
        self.sha512_solicitacao = None

    @property
    def pode_aceitar(self):
        documentos_entregues = [x.documentacao.id for x in self.documento_set.all()]
        return not DocumentoExigido.objects.filter(edital=self.selecionado.chamada.edital).exclude(documentacao_id__in=documentos_entregues).exists()    
    
    def save(self):
        print('SAVE', self.aceitou_algum_termo, self.aceitou_todos_termos)
        # Se aceitou apenas parte dos termos
        if self.aceitou_algum_termo and not self.aceitou_todos_termos:
            raise ValidationError("Tem que aceitar tanto o termo de veracidade das informações"
                                  " quanto o termo de ciência de que não poderá mais fazer alterações.")

        # Se aceitou todos os termos
        if self.aceitou_algum_termo and self.aceitou_todos_termos:
            self.enviada_em = now()
            self.sha512_solicitacao = None
            self.salvo_em = None

            self_str = serializers.serialize('json', [self])
            documentos = Documento.objects.filter(solicitacao_id=self.id).order_by('id')
            documentos_str = json.dumps([ {"documentacao_id": d.documentacao.id, 'arquivo': d.sha512_arquivo} for d in documentos])
            json_str = self_str + documentos_str
            self.sha512_solicitacao = hashlib.sha512(json_str.encode()).hexdigest()
        super().save()

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

    def save(self):
        self.sha512_arquivo = "-"
        super().save()
        hasher = hashlib.sha512()
        with self.arquivo.open(mode='rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        self.sha512_arquivo = hasher.hexdigest()
        super().save()
    
    def delete(self):
        self.arquivo.delete(False) 
        super().delete()
