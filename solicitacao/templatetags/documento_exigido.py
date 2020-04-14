from django import template
from ..models import Documento

register = template.Library()

@register.simple_tag
def ocorreu_upload(solicitacao_id, documentacao_id):
    doc = Documento.objects.filter(solicitacao_id=solicitacao_id, documentacao_id=documentacao_id)
    if len(doc) > 0:
        return 'Enviado'
    else:
        return 'Pendente'