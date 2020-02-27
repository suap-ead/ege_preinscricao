from django.db import models

class Responsavel(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=50)
  apelido = models.CharField(max_length=50)
  
  def __str__(self):
    return self.titulo