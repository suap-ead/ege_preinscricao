
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from .models import Selecionado, Solicitacao


class SelecionadoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        selecionado_id = request.session.get("selecionado_id", None)
        if selecionado_id:
            request.selecionado = Selecionado.objects.select_related(
                'chamada', 
                'chamada__edital', 
                'matriz_curso', 
                'ano_letivo', 
                'periodo_letivo', 
                'turno', 
                'forma_ingresso', 
                'polo', 
                'nacionalidade', 
                'convenio', 
                'cota_sistec', 
                'cota_mec', 
                'solicitacao',
            ).filter(id=selecionado_id).first()
            # request.selecionado.solicitacao.select_related(
            #     'linha_pesquisa',
            #     'sexo',
            #     'estado_civil',
            #     'estado_civil_pai',
            #     'estado_civil_mae',
            #     'parentesco_responsavel',
            #     'cidade',
            #     'estado',
            #     'tipo_zona_residencial',
            #     'tipo_necessidade_especial',
            #     'tipo_transtorno',
            #     'superdotacao',
            #     'poder_publico_responsavel_transporte',
            #     'tipo_veiculo',
            #     'tipo_sanguineo',
            #     'pais_origem',
            #     'estado_naturalidade',
            #     'naturalidade',
            #     'raca',
            #     'tipo_instituicao_origem',
            #     'ano_conclusao_estudo_anterior',
            #     'uf_emissao_rg',
            #     'orgao_emissao_rg',
            #     'uf_emissao_titulo_eleitor',
            #     'estado_emissao_carteira_reservista',
            #     'nivel_ensino_anterior',
            #     'tipo_certidao',)
