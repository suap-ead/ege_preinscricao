from import_export import resources
from .models import Candidato

class CandidatoResource(resources.ModelResource):
    class Meta:
        model = Candidato

