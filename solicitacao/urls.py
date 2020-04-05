from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from .views import index, selecionado, solicitacao

app_name = 'solicitacao'
urlpatterns = [
    path('', index, name='index'),
    path('selecionado', selecionado, name='selecionado'),
    path('solicitacao', solicitacao, name='solicitacao'),
]
