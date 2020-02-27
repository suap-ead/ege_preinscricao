from django.db import models

class Sexo(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=200)
  apelido = models.CharField(max_length=1)
  
  def __str__(self):
    return self.titulo