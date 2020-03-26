from django.db import models

class EmissaoRg(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=70)
  
  def __str__(self):
    return self.titulo