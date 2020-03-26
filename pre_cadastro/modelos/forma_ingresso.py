from django.db import models

class FormaIngresso(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=150)
  
  def __str__(self):
    return self.titulo