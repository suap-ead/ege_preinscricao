from django.db import models

class TipoInstituicao(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=30)
  apelido = models.CharField(max_length=30)
  
  def __str__(self):
    return self.titulo