from django.db import models

class TipoCertidao(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=25)
  
  def __str__(self):
    return self.titulo