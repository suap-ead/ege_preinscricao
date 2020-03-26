from django.db import models

class NecessidadeEspecial(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=50)
  
  def __str__(self):
    return self.titulo