from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from .views import auth_entrar, auth_autenticar, auth_sair
from .views import solicitacao_index, solicitacao_formulario, solicitacao_anexar, documento_remover, solicitacao_concluir

app_name = 'solicitacao'
urlpatterns = [
    path('', solicitacao_index, name='index'),
    path('<int:chamada_id>/', solicitacao_formulario, name='formulario'),
    path('<int:chamada_id>/concluir/', solicitacao_concluir, name='concluir'),
    path('<int:chamada_id>/anexar/', solicitacao_anexar, name='anexar'),
    path('documento/<int:documento_id>/remover/', documento_remover, name='documento_remove'),
    path('<int:chamada_id>/auth/entrar/', auth_entrar, name='auth_entrar'),
    path('<int:chamada_id>/auth/<slug:inscricao>/<slug:token>/autenticar/', auth_autenticar, name='auth_autenticar'),
    path('auth/sair/', auth_sair, name='auth_sair'),
]
