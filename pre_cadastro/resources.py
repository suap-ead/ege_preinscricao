from import_export import resources
from .modelos.candidato import Candidato

class CandidatoResource(resources.ModelResource):
    class Meta:
        model = Candidato

