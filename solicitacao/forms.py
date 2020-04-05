from django import forms

from .models import Selecionado, Solicitacao

class SelecionadoForm(forms.ModelForm):

    class Meta:
        model = Selecionado
        fields = ['chamada', 'matriz_curso', 'ano_letivo', 'periodo_letivo',
            'turno', 'forma_ingresso', 'polo', 'lista', 'nacionalidade',
            'cpf', 'passaporte', 'nome', 'nome_social', 'email', 'inscricao']

class SolicitacaoForm(forms.ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['cota_sistec', 'cota_mec', 'convenio', 'data_conclusao_intercambio',
            'linha_pesquisa', 'aluno_especial', 'nacionalidade', 'cpf', 'passaporte',
            'nome', 'nome_social', 'sexo', 'data_nascimento', 'estado_civil', 'nome_pai',
            'estado_civil_pai', 'pai_falecido', 'nome_mae', 'estado_civil_mae',
            'mae_falecida', 'responsavel', 'email_responsavel', 'parentesco_responsavel',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'tipo_zona_residencial', 'telefone_principal', 'telefone_secundario',
            'telefone_adicional_1', 'telefone_adicional_2', 'email_pessoal', 'aluno_pne',
            'tipo_necessidade_especial', 'tipo_transtorno', 'superdotacao',
            'utiliza_transporte_escolar_publico', 'poder_publico_responsavel_transporte',
            'tipo_veiculo', 'tipo_sanguineo', 'pais_origem', 'estado_naturalidade',
            'naturalidade', 'raca', 'nivel_ensino_anterior', 'tipo_instituicao_origem',
            'ano_conclusao_estudo_anterior', 'numero_rg', 'uf_emissao_rg',
            'orgao_emissao_rg', 'data_emissao_rg', 'numero_titulo_eleitor',
            'zona_titulo_eleitor', 'secao', 'data_emissao_titulo_eleitor',
            'uf_emissao_titulo_eleitor', 'numero_carteira_reservista',
            'regiao_carteira_reservista', 'serie_carteira_reservista',
            'estado_emissao_carteira_reservista', 'nivel_ensino_anterior',
            'ano_carteira_reservista', 'tipo_certidao', 'numero_certidao',
            'folha_certidao', 'livro_certidao', 'data_emissao_certidao',
            'matricula_certidao', 'autorizacao_carteira_estudantil', 'enviada_em',
            'sha512_foto', 'sha512_solicitacao']