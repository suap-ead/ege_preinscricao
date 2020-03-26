from django.db import models

class TransportePublico(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=10)
  apelido = models.CharField(max_length=10)
  
  def __str__(self):
    return self.titulo