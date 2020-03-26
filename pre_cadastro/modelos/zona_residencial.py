from django.db import models

class ZonaResidencial(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=40)
  
  def __str__(self):
    return self.titulo