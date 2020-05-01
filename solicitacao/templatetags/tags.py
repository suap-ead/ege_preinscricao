from django import template
from ..settings import *

register = template.Library()

@register.simple_tag
def footer_text(request):
    return FOOTER_TEXT