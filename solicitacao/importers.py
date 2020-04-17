import datetime
import csv
import re
from dominio_suap.models import Polo, MatrizCurso, Turno, AnoLetivo, PeriodoLetivo, Nacionalidade
from .models import Chamada, Selecionado, ListaSelecao


polos = {x.titulo: x.id for x in Polo.objects.all()}
cursos = {x.titulo: x.id for x in MatrizCurso.objects.all()}
turnos = {x.titulo: x.id for x in Turno.objects.all()}


SELECIONADO_POLO = 'Campus'
SELECIONADO_CURSO = 'Curso'
SELECIONADO_TURNO = 'Turno'
SELECIONADO_INSCRICAO = 'Inscrição'
SELECIONADO_NOME = 'Candidato'
SELECIONADO_CPF = 'CPF'
SELECIONADO_RG_NUMERO = 'Documento de Identificação'
SELECIONADO_RG_ORGAO = 'Orgão Expeditor do Documento de Identificação'
SELECIONADO_RG_UF = 'UF do Documento de Identificação'
SELECIONADO_RG_EMISSAO = 'Data da Emissão do Documento de Identificação'
SELECIONADO_DATA_NASCIMENTO = 'Data de Nascimento'
SELECIONADO_ENDERECO = 'Endereço'
SELECIONADO_TELEFONE1 = 'Telefone 1'
SELECIONADO_TELEFONE2 = 'Telefone 2'
SELECIONADO_EMAIL = 'Email'
SELECIONADO_ESCOLA_PUBLICA = 'Escola Pública'
SELECIONADO_ETINIA = 'Etnia'
SELECIONADO_RENDA = 'Renda'
SELECIONADO_DEFICIENCIA_FISICA = 'Deficência Física'
SELECIONADO_STATUS = 'Status'
SELECIONADO_ESCORE = 'Escore'
SELECIONADO_ANALISE_CURRICULAR = 'Análise Curricular'
SELECIONADO_CLASSIFICACAO_GERAL = 'Classificação Geral'
SELECIONADO_CLASSIFICACAO_PPI = 'Classificação PPI'
SELECIONADO_CLASSIFICACAO_PCD = 'Classificação PCD'

SELECIONADO_COLUMNS = [
    {'COLUMN': SELECIONADO_POLO, 'FIELD': 'polo_id', 'LOOKUP': polos},
    {'COLUMN': SELECIONADO_CURSO, 'FIELD': 'matriz_curso_id', 'LOOKUP': cursos},
    {'COLUMN': SELECIONADO_TURNO, 'FIELD': 'turno_id', 'LOOKUP': turnos},
    {'COLUMN': SELECIONADO_INSCRICAO, 'FIELD': 'inscricao'},
    {'COLUMN': SELECIONADO_NOME, 'FIELD': 'nome'},
    {'COLUMN': SELECIONADO_CPF, 'FIELD': 'cpf'},
    {'COLUMN': SELECIONADO_RG_NUMERO, 'FIELD': None},
    {'COLUMN': SELECIONADO_RG_ORGAO, 'FIELD': None},
    {'COLUMN': SELECIONADO_RG_UF, 'FIELD': None},
    {'COLUMN': SELECIONADO_RG_EMISSAO, 'FIELD': None},
    {'COLUMN': SELECIONADO_DATA_NASCIMENTO, 'FIELD': None},
    {'COLUMN': SELECIONADO_ENDERECO, 'FIELD': None},
    {'COLUMN': SELECIONADO_TELEFONE1, 'FIELD': None},
    {'COLUMN': SELECIONADO_TELEFONE2, 'FIELD': None},
    {'COLUMN': SELECIONADO_EMAIL, 'FIELD': 'email'},
    {'COLUMN': SELECIONADO_ESCOLA_PUBLICA, 'FIELD': None},
    {'COLUMN': SELECIONADO_ETINIA, 'FIELD': None},
    {'COLUMN': SELECIONADO_RENDA, 'FIELD': None},
    {'COLUMN': SELECIONADO_DEFICIENCIA_FISICA, 'FIELD': None},
    {'COLUMN': SELECIONADO_STATUS, 'FIELD': None},
    {'COLUMN': SELECIONADO_ESCORE, 'FIELD': None},
    {'COLUMN': SELECIONADO_ANALISE_CURRICULAR, 'FIELD': None},
    {'COLUMN': SELECIONADO_CLASSIFICACAO_GERAL, 'FIELD': None},
    {'COLUMN': SELECIONADO_CLASSIFICACAO_PPI, 'FIELD': None},
    {'COLUMN': SELECIONADO_CLASSIFICACAO_PCD, 'FIELD': None}
]


def selecionado_csv_importer(chamada_id, filename, forma_ingresso_id=50):
    """
    'Classificação Geral'
    'Classificação PPI'
    'Classificação PCD'
    """
    chamada = Chamada.objects.get(id=chamada_id)
    ano_letivo = AnoLetivo.objects.get(titulo='2020')
    periodo_letivo = PeriodoLetivo.objects.get(titulo='1')
    nacionalidade = Nacionalidade.objects.get(titulo='Brasileira')
    qtd = 0

    with open('selecionados.csv', newline='') as csvfile:
        polo_key = '\ufeffCampus'
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            if row['Status'] != 'Aprovado':
                continue

            qtd += 1

            selecionado = Selecionado.objects.filter(chamada_id=chamada_id, cpf=row['CPF']).first()
            if selecionado is None:
                selecionado = Selecionado()

            selecionado.chamada_id = chamada_id
            selecionado.ano_letivo = ano_letivo
            selecionado.periodo_letivo = periodo_letivo
            selecionado.nacionalidade = nacionalidade
            selecionado.forma_ingresso_id = forma_ingresso_id
            if row['Classificação PPI'] != '-':
                selecionado.lista = ListaSelecao.PPI
            elif row['Classificação PCD'] != '-':
                selecionado.lista = ListaSelecao.PCD
            elif row['Classificação Geral'] != '-':
                selecionado.lista = ListaSelecao.GERAL
            else:
                raise Exception("Lista não identificada %s " % row)

            for col in SELECIONADO_COLUMNS:
                if col['FIELD'] is not None:
                    fix_excel_name = "\ufeff" + col["COLUMN"] if '\ufeff' + col["COLUMN"] in row else col["COLUMN"]
                    val = row[fix_excel_name]
                    if 'LOOKUP' in col:
                        val = col["LOOKUP"][val]
                    if fix_excel_name == 'CPF':
                        val = re.sub('\D', '', val)
                    setattr(selecionado, col['FIELD'], val)
            selecionado.save()
    print(qtd)
