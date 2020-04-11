from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from .views import index, entrar, autenticar, sair, solicitacao, remove_documento, adicionar_documento

app_name = 'solicitacao'
urlpatterns = [
    path('', index, name='index'),
    path('<int:chamada_id>/acesso/entrar/', entrar, name='entrar'),
    path('<int:chamada_id>/<slug:inscricao>/<slug:token>/autenticar/', autenticar, name='autenticar'),
    path('acesso/sair/', sair, name='sair'),
    path('<int:chamada_id>/solicitacao/', solicitacao, name='solicitacao'),
    path('<int:documento_id>/remove_documento/', remove_documento, name='remove_documento'),
    path('adicionar_documento/', adicionar_documento, name='adicionar_documento'),
]
