from django.db import models

class PeriodoLetivo(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=20)
  
  def __str__(self):
    return self.titulo